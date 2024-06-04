from sqlalchemy.sql.expression import union_all

from CTFd.utils.modes import get_model
from CTFd.cache import cache
from CTFd.models import Awards, Challenges, Solves, db
from CTFd.utils import app, get_config
from CTFd.utils.dates import unix_time_to_utc

from ..models import Campuses, Users


@cache.memoize(timeout=60)
def get_standings(count=None, campus_id=None, admin=False, fields=None):
    """
    Get standings as a list of tuples containing account_id, name, and score e.g. [(account_id, team_name, score)].

    Ties are broken by who reached a given score first based on the solve ID. Two users can have the same score but one
    user will have a solve ID that is before the others. That user will be considered the tie-winner.

    Challenges & Awards with a value of zero are filtered out of the calculations to avoid incorrect tie breaks.
    """
    if fields is None:
        fields = []

    scores = (
        db.session.query(
            Solves.account_id.label("account_id"),
            db.func.sum(Challenges.value).label("score"),
            db.func.max(Solves.id).label("id"),
            db.func.max(Solves.date).label("date"),
        )
        .join(Challenges)
        .filter(Challenges.value != 0)
        .group_by(Solves.account_id)
    )

    awards = (
        db.session.query(
            Awards.account_id.label("account_id"),
            db.func.sum(Awards.value).label("score"),
            db.func.max(Awards.id).label("id"),
            db.func.max(Awards.date).label("date"),
        )
        .filter(Awards.value != 0)
        .group_by(Awards.account_id)
    )

    """
    Filter out solves and awards that are before a specific time point.
    """
    freeze = get_config("freeze")
    if not admin and freeze:
        scores = scores.filter(Solves.date < unix_time_to_utc(freeze))
        awards = awards.filter(Awards.date < unix_time_to_utc(freeze))

    """
    Combine awards and solves with a union. They should have the same amount of columns
    """
    results = union_all(scores, awards).alias("results")

    """
    Sum each of the results by the team id to get their score.
    """
    sumscores = (
        db.session.query(
            results.columns.account_id,
            db.func.sum(results.columns.score).label("score"),
            db.func.max(results.columns.id).label("id"),
            db.func.max(results.columns.date).label("date"),
        )
        .group_by(results.columns.account_id)
        .subquery()
    )

    """
    Admins can see scores for all users but the public cannot see banned users.

    Filters out banned users.
    Properly resolves value ties by ID.

    Different databases treat time precision differently so resolve by the row ID instead.
    """
    if admin:
        standings_query = (
            db.session.query(
                Users.id.label("account_id"),
                Users.oauth_id.label("oauth_id"),
                Users.name.label("name"),
                Users.campus_id.label("campus_id"),
                Campuses.name.label("campus_name"),
                Users.hidden,
                Users.banned,
                sumscores.columns.score,
                *fields,
            )
            .join(sumscores, Users.id == sumscores.columns.account_id)
            .join(Campuses, isouter=True)
            .order_by(
                sumscores.columns.score.desc(),
                sumscores.columns.date.asc(),
                sumscores.columns.id.asc(),
            )
        )
    else:
        standings_query = (
            db.session.query(
                Users.id.label("account_id"),
                Users.oauth_id.label("oauth_id"),
                Users.name.label("name"),
                Users.campus_id.label("campus_id"),
                Campuses.name.label("campus_name"),
                sumscores.columns.score,
                *fields,
            )
            .join(sumscores, Users.id == sumscores.columns.account_id)
            .join(Campuses, isouter=True)
            .filter(Users.banned == False, Users.hidden == False)
            .order_by(
                sumscores.columns.score.desc(),
                sumscores.columns.date.asc(),
                sumscores.columns.id.asc(),
            )
        )

    # Filter on a campus if asked
    if campus_id is not None:
        standings_query = standings_query.filter(Users.campus_id == campus_id)

    # Only select a certain amount of users if asked.
    if count is None:
        standings = standings_query.all()
    else:
        standings = standings_query.limit(count).all()

    return standings


@cache.memoize(timeout=60)
def get_campus_rankings(admin=None):
    Model = get_model()

    # Récupérer tous les campuses
    all_campuses = app.db.session.query(
        Campuses.id.label("campus_id"),
        Campuses.name.label("campus_name"),
        Campuses.slug.label("campus_slug"),
    ).all()

    # Initialiser un dictionnaire pour stocker les scores par campus
    campus_scores = {
        campus.campus_id: {
            'campus_name': campus.campus_name,
            'total_score': 0,
            'campus_slug': campus.campus_slug,
        } for campus in all_campuses
    }

    # Récupérer les standings de tous les utilisateurs
    standings = get_standings()
    print("STANDINGS: ", standings)

    # Grouper les scores par campus
    for standing in standings:
        campus_id = standing.campus_id
        score = standing.score
        if campus_id in campus_scores:
            campus_scores[campus_id]['total_score'] += score

    # Convertir le dictionnaire en liste de tuples et trier par score total décroissant
    sorted_campuses = sorted(campus_scores.items(), key=lambda x: x[1]['total_score'], reverse=True)

    return sorted_campuses

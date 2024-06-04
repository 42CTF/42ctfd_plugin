from CTFd.utils import app

from ..models import Campuses, Users


def get_campus(_filter, admin=False):
    campus = (
        app.db.session.query(
            Campuses.id.label("id"),
            Campuses.name.label("name"),
            Campuses.slug.label("slug"),
        )
        .filter(_filter)
        .first()
    )

    if campus is None:
        return None

    users_object = (
        app.db.session.query(
            Users.id.label("id"),
            Users.name.label("name"),
            Users.email.label("email"),
            *[
                Users.hidden.label("hidden") if admin else None,
                Users.banned.label("banned") if admin else None,
            ],
            Users.verified.label("verified"),
            Campuses.name.label("campus"),
        )
        .join(Campuses)
        .filter(
            Users.campus_id == campus.id,
            (not Users.hidden) if not admin else True,
            (not Users.banned) if not admin else True,
        )
        .all()
    )

    from .scores import get_standings

    standings = get_standings()
    campus_standings = [
        standing for standing in standings if standing.campus_id == campus.id
    ]
    campus_score = sum([standing.score for standing in campus_standings])

    return {
        **dict(campus),
        "score": int(campus_score),
        "users": [dict(user) for user in users_object],
    }

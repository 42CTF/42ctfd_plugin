from CTFd.utils import app

from ..models import Campuses, Users
from .scores import get_standings


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
            (Users.hidden == False) if not admin else True,  # noqa: E712
            (Users.banned == False) if not admin else True,  # noqa: E712
        )
        .all()
    )

    standings = get_standings(campus_id=campus.id)

    return {
        **dict(campus),
        "score": int(sum([standing.score for standing in standings])),
        "users": [dict(user) for user in users_object],
    }

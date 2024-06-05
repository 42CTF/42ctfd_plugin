from CTFd.scoreboard import scoreboard as scoreboard_blueprint
from CTFd.utils import config
from CTFd.utils.config.visibility import scores_visible
from CTFd.utils.decorators.visibility import (
    check_account_visibility,
    check_score_visibility,
)
from CTFd.utils.helpers import get_infos
from CTFd.utils.user import is_admin
from flask import render_template

from .utils import get_campus_rankings, get_standings, unregister_route
from .utils.decorators import ft_theme


def init(app):
    @scoreboard_blueprint.route("/scoreboard/global", endpoint="global")
    @ft_theme()
    @check_account_visibility
    @check_score_visibility
    def scoreboard_global():
        infos = get_infos()

        if config.is_scoreboard_frozen():
            infos.append("Scoreboard has been frozen")

        if is_admin() is True and scores_visible() is False:
            infos.append("Scores are not currently visible to users")

        standings = get_standings()

        return render_template(
            "scoreboard/global.html", standings=standings, infos=infos
        )

    @scoreboard_blueprint.route("/scoreboard/campus", endpoint="campus")
    @ft_theme()
    @check_account_visibility
    @check_score_visibility
    def scoreboard_campus():
        infos = get_infos()

        if config.is_scoreboard_frozen():
            infos.append("Scoreboard has been frozen")

        if is_admin() is True and scores_visible() is False:
            infos.append("Scores are not currently visible to users")

        campuses = get_campus_rankings()

        podium = campuses[:3]
        for i in range(3 - len(podium)):
            podium.append(
                (
                    None,
                    {
                        "campus_name": "N/A",
                        "total_score": 0,
                        "campus_slug": None,
                    },
                )
            )

        return render_template(
            "scoreboard/campus.html", infos=infos, campuses=campuses, podium=podium
        )

    app.register_blueprint(scoreboard_blueprint)
    unregister_route(app, "scoreboard.listing")

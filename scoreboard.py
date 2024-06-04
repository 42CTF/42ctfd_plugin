from flask import render_template

from CTFd.utils import config
from CTFd.utils.config.visibility import scores_visible
from CTFd.utils.decorators.visibility import (
    check_account_visibility,
    check_score_visibility,
)
from CTFd.utils.helpers import get_infos
from CTFd.utils.user import is_admin
from CTFd.scoreboard import scoreboard as scoreboard_blueprint

from .utils import unregister_route, get_standings, get_campus_rankings


def init(app):
    @scoreboard_blueprint.route("/scoreboard/global", endpoint="global")
    @check_account_visibility
    @check_score_visibility
    def scoreboard_global():
        infos = get_infos()

        if config.is_scoreboard_frozen():
            infos.append("Scoreboard has been frozen")

        if is_admin() is True and scores_visible() is False:
            infos.append("Scores are not currently visible to users")

        standings = get_standings()
        return render_template("scoreboard/global.html", standings=standings, infos=infos)

    @scoreboard_blueprint.route("/scoreboard/campus", endpoint="campus")
    @check_account_visibility
    @check_score_visibility
    def scoreboard_campus():
        infos = get_infos()

        if config.is_scoreboard_frozen():
            infos.append("Scoreboard has been frozen")

        if is_admin() is True and scores_visible() is False:
            infos.append("Scores are not currently visible to users")

        campuses = get_campus_rankings()

        for campus in campuses:
            campus[1]['campus_logo'] = f'images/logos/{campus[1]["campus_slug"]}.svg'
            campus[1]['campus_url'] = f'/campus/{campus[1]["campus_slug"]}'

        podium = campuses[:3]
        for i in range(3 - len(podium)):
            podium.append((None, {
                'campus_name': 'N/A',
                'total_score': 0,
                'campus_slug': None,
                'campus_logo': None,
                'campus_url': '#'
            }))

        print("BRACKETS: ", campuses)
        return render_template("scoreboard/campus.html", infos=infos, campuses=campuses, podium=podium)

    app.register_blueprint(scoreboard_blueprint)
    unregister_route(app, 'scoreboard.listing')
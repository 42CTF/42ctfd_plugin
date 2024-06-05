from CTFd.utils.decorators import admins_only, authed_only
from flask import render_template

from ..utils.decorators import ft_theme


def init(app):
    @app.route("/admin/campus", methods=["GET"])
    @ft_theme(admin=True)
    @authed_only
    @admins_only
    def admin_campus():
        return render_template("admin/campus.html")

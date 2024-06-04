from CTFd.utils.decorators import admins_only, authed_only
from flask import render_template


def init(app):
    @app.route("/admin/campus", methods=["GET"])
    @authed_only
    @admins_only
    def admin_campus():
        return render_template("admin/campus.html")

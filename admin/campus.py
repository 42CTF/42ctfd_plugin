from flask import render_template
from CTFd.utils.decorators import authed_only, admins_only


def init(app):
    @app.route("/admin/campus", methods=["GET"])
    @authed_only
    @admins_only
    def admin_campus():
        return render_template("admin/campus.html")

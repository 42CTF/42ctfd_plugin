from pathlib import Path
from CTFd.utils.plugins import override_template
from CTFd.api import CTFd_API_v1
from CTFd.plugins.migrations import upgrade

from .translate import init as init_babel
from .scoreboard import init as init_scoreboard
from .admin.campus import init as init_admin_campus
from .api.v1.campuses import campuses_namespace
from .models import Users, Campuses
from .schemas.campuses import CampusSchema


def load(app):
    # Init the translation module
    init_babel(app)

    # Init the scoreboard module
    init_scoreboard(app)

    # Init the campus management module
    init_admin_campus(app)

    # Create the Campuses model in database
    app.db.create_all()
    # Perform the migration if not done yet
    upgrade()

    # Add the api namespace campuses
    CTFd_API_v1.add_namespace(campuses_namespace, "/campuses")

    # Add the make the admin/campus template accessible through 'admin/campus.html'
    # parent.parent.parent seems a bit dirty to me,
    # TODO: maybe find a better way to add the admin/campus template
    dir_path = Path(__file__).parent.parent.parent.resolve()
    template_path = dir_path / 'themes' / '42ctf' / 'templates' / 'admin' / 'campus.html'
    override_template('admin/campus.html', open(template_path).read())

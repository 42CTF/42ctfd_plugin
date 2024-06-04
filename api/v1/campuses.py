from CTFd.api.v1.helpers.request import validate_args
from CTFd.constants import RawEnum
from CTFd.models import db
from CTFd.utils.decorators import admins_only
from CTFd.utils.helpers.models import build_model_filters
from CTFd.utils.user import is_admin
from flask import request
from flask_restx import Namespace, Resource

from ...models import Campuses
from ...schemas.campuses import CampusSchema
from ...utils import get_campus

campuses_namespace = Namespace("campuses", description="Endpoint to retrieve Campuses")


@campuses_namespace.route("")
class CampusList(Resource):
    @validate_args(
        {
            "name": (str, None),
            "description": (str, None),
            "slug": (str, None),
            "q": (str, None),
            "field": (
                RawEnum(
                    "CampusFields",
                    {"name": "name", "description": "description", "slug": "slug"},
                ),
                None,
            ),
        },
        location="query",
    )
    def get(self, query_args):
        q = query_args.pop("q", None)
        field = str(query_args.pop("field", None))
        filters = build_model_filters(model=Campuses, query=q, field=field)

        campuses = (
            db.session.query(Campuses).filter_by(**query_args).filter(*filters).all()
        )
        schema = CampusSchema(many=True)
        response = schema.dump(campuses)
        if response.errors:
            return {"success": False, "errors": response.errors}, 400
        return {"success": True, "data": response.data}

    @admins_only
    def post(self):
        req = request.get_json()
        schema = CampusSchema()
        response = schema.load(req, session=db.session)

        if response.errors:
            return {"success": False, "errors": response.errors}, 400

        db.session.add(response.data)
        db.session.commit()

        response = schema.dump(response.data)
        db.session.close()

        return {"success": True, "data": response.data}


@campuses_namespace.route("/<int:campus_id>")
class Campus(Resource):
    def get(self, campus_id):
        campus = get_campus(Campuses.id == campus_id, admin=is_admin())
        if not campus:
            return {"success": False, "message": "Campus not found"}, 404
        return {"success": True, "data": campus}

    @admins_only
    def patch(self, campus_id):
        campus = Campuses.query.filter_by(id=campus_id).first_or_404()
        schema = CampusSchema()

        req = request.get_json()

        response = schema.load(req, session=db.session, instance=campus)
        if response.errors:
            return {"success": False, "errors": response.errors}, 400

        db.session.commit()

        response = schema.dump(response.data)
        db.session.close()

        return {"success": True, "data": response.data}

    @admins_only
    def delete(self, campus_id):
        campus = Campuses.query.filter_by(id=campus_id).first_or_404()
        db.session.delete(campus)
        db.session.commit()
        db.session.close()

        return {"success": True}

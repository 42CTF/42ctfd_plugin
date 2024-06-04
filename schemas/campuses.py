from CTFd.models import ma
from ..models import Campuses


class CampusSchema(ma.ModelSchema):
    class Meta:
        model = Campuses
        include_fk = True
        dump_only = ("id",)

from CTFd.models import db


class Users(db.Model):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    campus_id = db.Column(
        db.Integer,
        db.ForeignKey("campuses.id", ondelete="SET NULL")
    )

class Campuses(db.Model):
    __tablename__ = "campuses"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)

    def get_logo_template(self):
        return f"images/logos/{self.slug}.svg"
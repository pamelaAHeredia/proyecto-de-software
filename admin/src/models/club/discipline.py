from src.models.database import db


class Discipline(db.Model):
    __tablename__ = "discipline"
    __table_args__ = (
        db.UniqueConstraint("name", "category", name="unique_discipline_name_category"),
    )
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    category = db.Column(db.String(255), nullable=False)
    instructor_first_name = db.Column(db.String(75), nullable=False)
    instructor_last_name = db.Column(db.String(75), nullable=False)
    days_and_schedules = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    deleted = db.Column(db.Boolean, default=False)

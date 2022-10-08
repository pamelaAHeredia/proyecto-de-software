from src.models.database import db


class Discipline(db.Model):
    """
    A class used to represent a Discipline

    Attributes
    ---------
    name : str
        Discipline name.
    category : str
        Category name. It's a subdivision of the discipline.
    instructor_first_name : str
        Name of the instructor who teaches the discipline.
    instructor_last_name : str
        Last name of the instructor who teaches the discipline.
    days_and_schedules : str
        Days and times that the discipline is practiced.
    amount : Decimal(10, 2)
        Amount to pay for practicing the discipline.
    is_active : Boolean
        Discipline activity status. True for active.
    deleted : Boolean
        If the discipline is deleted (logical) then True.
    """

    __tablename__ = "discipline"
    __table_args__ = (
        db.UniqueConstraint("name", "category", name="unique_discipline_name_category"),
    )
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    instructor_first_name = db.Column(db.String(75), nullable=False)
    instructor_last_name = db.Column(db.String(75), nullable=False)
    days_and_schedules = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    deleted = db.Column(db.Boolean, default=False)
    
    def __init__(self, name, category, instructor_first_name, instructor_last_name, days_and_schedules, amount=0, is_active=True):
        self.name = name
        self.category = category
        self.instructor_first_name = instructor_first_name
        self.instructor_last_name = instructor_last_name
        self.days_and_schedules = days_and_schedules
        self.amount = amount
        self.is_active = is_active
    
    def __repr__(self):
        return f'<Disciplina {self.name} {self.category}>'
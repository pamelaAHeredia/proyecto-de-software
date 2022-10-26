from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.models.database import db


class Discipline(db.Model):
    """
    Clase usada para representar una Disciplina

    Atributos
    ---------
    name : str
        Nombre de la disciplina.
    category : str
        Nombre de la categoria. Es una subdivisión de la disciplina.
    instructor_first_name : str
        Nombre del instructor que enseña la disciplina.
    instructor_last_name : str
        Apellido del instructor que enseña la disciplina.
    days_and_schedules : str
        Días y horarios en la que la disciplina se dicta.
    deleted : Boolean
        Indica si la disciplina se sigue dando o no.
    """

    __tablename__ = "discipline"
    # __table_args__ = (
    #     db.UniqueConstraint("name", "category", name="unique_discipline_name_category"),
    # )
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    instructor = db.Column(db.String(255), nullable=False)
    days_and_schedules = db.Column(db.String(100), nullable=False)
    membership = db.relationship(
        "Membership", back_populates="discipline", uselist=False
    )
    deleted = db.Column(db.Boolean, default=False)

    def __init__(
        self,
        name,
        category,
        instructor,
        days_and_schedules,
    ):
        self.name = name
        self.category = category
        self.instructor = instructor
        self.days_and_schedules = days_and_schedules

    @property
    def amount(self):
        return self.membership.amount

    @property
    def is_active(self):
        return self.membership.is_active

    @is_active.setter
    def is_active(self, v):
        self.membership.is_active = v

    @property
    def pays_per_year(self):
        return self.membership.pays_per_year

    @pays_per_year.setter
    def pays_per_year(self, v):
        self.membership.pays_per_year = v

    @property
    def registration_quota(self):
        return self.membership.registration_quota

    @property
    def has_quota(self):
        return self.membership.has_quota

    @registration_quota.setter
    def registration_quota(self, v):
        self.membership.registration_quota = v

    @property
    def discipline_name(self):
        return f"{self.name} {self.category}"

    def __repr__(self):
        return f"<Disciplina {self.name} {self.category}>"


class DisciplineSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Discipline
        include_relationships = False
        load_instance = True

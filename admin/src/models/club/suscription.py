from src.models.database import db


class Suscription(db.Model):
    """
    Clase usada para representar una inscripcion a una membresia por parte de un socio

    Atributos
    ---------
    date_from : Datetime
        Fecha en la que se realizó la inscripción.
    date_from : Datetime
        Fecha en la que se realizó la baja de la inscripción.
    membership_id : Integer
        Es el Id de la membresia asociada a la suscripcion.
    membership : Membership
        Es el objeto membresia que contiene la relación.
    member_id : Integer
        Es el Id del socio asociado a la suscripcion.
    membership : Member
        Es el objeto socio que contiene la relación.
    
    """

    __tablename__ = "suscription"
    __table_args__ = (
        db.UniqueConstraint("membership_id", name="unique_membership_id"),
    )
    id = db.Column(db.Integer, primary_key=True, unique=True)
    date_from = db.Column(db.DateTime, default=datetime.datetime.now)
    date_to = db.Column(db.DateTime, nullable=True)
    membership_id = db.Column(db.Integer, db.ForeignKey("membership.id"))
    membership = db.relationship("Membership", back_populates="suscription")
    member_id = db.Column(db.Integer, db.ForeignKey("member.membership_number"))
    member = db.relationship("Member")

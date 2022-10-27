from math import perm
from src.models.database import db


# Define la tabla que relaciona Roles con Permisos
role_has_permission = db.Table('role_has_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

# Define la clase Rol
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(20))
    permissions = db.relationship(
        'Permission', 
        secondary=role_has_permission,
        lazy='subquery',
        backref=db.backref('roles', lazy=True)
        )

    def __init__(self, name):
        self.name = name

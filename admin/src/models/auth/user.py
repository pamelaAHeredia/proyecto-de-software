from src.models.database import db

user_has_role = db.Table('user_has_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

role_has_permission = db.Table('role_has_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(20))
    users = db.relationship("User", secondary="user_has_role", backref="role")

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    user_has_role = db.relationship('Role', secondary="user_has_role", backref='user')


class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    roles = db.relationship("Role", secondary="role_has_permission", backref="permission")
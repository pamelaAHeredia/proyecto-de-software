from src.models.database import db


# Define la tabla que relaciona Usuarios con Roles
user_has_role = db.Table(
    "user_has_role",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
)

# Define la clase Usuario
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    blocked = db.Column(db.Boolean, default=False)
    roles = db.relationship(
        "Role",
        secondary=user_has_role,
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )
    members = db.relationship("Member", back_populates="user", lazy="dynamic")

    def __init__(
        self,
        email,
        username,
        password,
        first_name,
        last_name,
        roles,
    ):
        self.email = email
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.roles = roles

    @property
    def is_admin(self):
        aux = False
        for role in self.roles: 
            if role.name == "Administrador":
                aux = True
        return aux
    
    @property
    def is_member(self):
        aux = False
        for role in self.roles: 
            if role.name == "Socio":
                aux = True
        return aux
    
    @property
    def is_main_admin(self): 
        """Función que devuelve si el usuario es el administrador principal."""
        return self.id == 1; 
     
    @property
    def has_members(self):
        """Función que devuelve true si el usuario tiene socios asignados."""
        return len(list(self.members)) > 0

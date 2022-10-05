from src.models.database import db
from src.models.club.member import Member


class MemberService:
    @classmethod
    def list_members(cls):
        """Función que retorna la lista de todos los Socios de la Base de Datos"""
        return Member.query.all()

    @classmethod
    def create_member(
        cls,
        first_name,
        last_name,
        document_type,
        document_number,
        gender,
        address,
        phone_number="",
        email="",
    ):
        """Función que instancia un Socio, lo agrega a la Base de Datos y lo retorna"""
        member = Member(
            first_name,
            last_name,
            document_type,
            document_number,
            gender,
            address,
            phone_number,
            email,
        )
        if not cls.find_member(document_type, document_number):
            db.session.add(member)
            db.session.commit()
            return member
        return None 

    @classmethod
    def find_member(cls, document_type, document_number):
        """Funcion que busca un socio en la base de datos por tipo y numero de documento"""
        return Member.query.filter_by(
            document_type=document_type, document_number=document_number, deleted=False
        ).first()

    @classmethod
    def get_by_membership_number(cls, id):
        """Funcion que retorna un Socio de la base de Datos por su Nro de Socio"""
        return Member.query.get(id)

from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from src.models.database import db
from src.models.club.member import Member
from src.errors import database
from src.services.paginator import Paginator


class MemberService:
    """Clase que representa el manejo de los Socios"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemberService, cls).__new__(cls)
        return cls._instance

    def list_members(self):
        """Función que retorna la query de todos los Socios de la Base de Datos ordenada por 
        Nro de Socio"""
        return Member.query.order_by(Member.membership_number)

    def list_paginated_members(
        self, page: int, items_per_page: int, endpoint: str, filter: str
    ) -> Paginator:
        """Función que retorna el paginador con los socios del sistema.

        Args:
           page: Número de pagina.
           items_per_page: cantidad de registros por página.
           endpoint: endpoint para el armado del url_for.

        Returns:
           Un paginador.
        """
        if filter == "Activos":
            members = self.list_by_is_active(active=True)
        elif filter == "Inactivos":
            members = self.list_by_is_active(active=False)   
        else:  
            members = self.list_members()
        return Paginator(members, page, items_per_page, endpoint)



    def create_member(
        self,
        first_name,
        last_name,
        document_type,
        document_number,
        gender,
        address,
        phone_number="",
        email="",
    ):
        """Función que instancia un Socio, lo agrega a la Base de Datos y lo retorna solo en caso
        de que no exista el tipo y numero de documento"""

        if not self.find_member(document_type, document_number):
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
            db.session.add(member)
            db.session.commit()
            return member
        raise database.ExistingData(info="ATENCION!!!",
            message="Ya existe el Socio con ese tipo y numero de documento"
        )

    def find_member(self, document_type, document_number):
        """Funcion que busca un socio en la base de datos por tipo y numero de documento"""
        return Member.query.filter_by(
            document_type=document_type, document_number=document_number, deleted=False
        ).first()

    def get_by_membership_number(self, id):
        """Funcion que retorna un Socio de la base de Datos por su Nro de Socio"""
        return Member.query.get(id)

    def update_member(
        self,
        id,
        first_name,
        last_name,
        document_type,
        document_number,
        gender,
        address,
        phone_number="",
        email="",
    ):
        """Función que actualiza un Socio modificando sus datos en la base, controla que
        no se duplique el tipo y numero de documento"""
        member_found = self.find_member(document_type, document_number)
        if not member_found or (id == member_found.membership_number):
            member = self.get_by_membership_number(id)
            member.first_name = first_name
            member.last_name = last_name
            member.document_type = document_type
            member.document_number = document_number
            member.gender = gender
            member.address = address
            member.phone_number = phone_number
            member.email = email
            db.session.commit()
            return member
        raise database.ExistingData(info="ATENCION!!!",
            message="Ya existe el Socio con ese tipo y numero de documento"
        )

    def deactivate_member(self, id):
        """Función que pone inactivo a un Socio"""
        member = self.get_by_membership_number(id)
        member.is_active = False
        db.session.commit()
        return member

    def list_by_last_name(self, substring):
        """Función que retorna la lista de todos los Socios que en su apellido tenga
        el substring enviado por parametro"""
        return Member.query.filter(Member.last_name.ilike("%" + substring + "%")).all()

    def list_by_is_active(self, active):
        """Función que retorna la lista de todos los Socios activos o inactivos
        segun el parametro enviado"""
        return Member.query.filter_by(is_active=active).order_by(Member.membership_number)
    

    def format_pdf(self, pdf):
        """Función que define el formato de las paginas del pdf"""
        pdf.drawImage('../admin/public/logoclub.jpg', 5, 790 , width=50, height=50)
        pdf.setFont("Helvetica", 20)
        pdf.setLineWidth(0.3)
        pdf.drawCentredString(300, 800, "Reporte de Asociados")
        pdf.setFontSize(15)
        pdf.drawString(5, 750, "#")
        pdf.drawString(60, 750, "Apellido")
        pdf.drawString(200, 750, "Nombre")
        pdf.drawString(350, 750, "Tipo y numero de documento")
        pdf.line(1, 740, 600, 740)
        pdf.setFontSize(12)
        pdf.drawString(490, 820, "Fecha: "+ date.today().strftime("%d/%m/%Y"))
        pdf.drawString(520, 10, "Página " + str(pdf.getPageNumber()))
        return pdf



    def export_list_to_pdf(self, members, line_per_page):
        """Funcion que exporta una lista de Socios a un archivo report.pdf"""
        pdf = canvas.Canvas("report.pdf", pagesize=A4)
        members_per_page = 0
        members_total = 0
        self.format_pdf(pdf)
        y = 725
        for member in members:
            pdf.drawString(5, y, str(member.membership_number))
            pdf.drawString(60, y, member.last_name)
            pdf.drawString(200, y, member.first_name)
            pdf.drawString(350, y, member.document_type + " " + member.document_number)
            y = y - 20
            members_per_page = members_per_page + 1
            members_total = members_total + 1
            if (line_per_page == members_per_page) and (members_total < len(members)):
               pdf.showPage()
               members_per_page = 0
               self.format_pdf(pdf)
               y = 725
        pdf.save()
        return pdf

    def no_user(self, id):
        """Funcion que retorna True si el Socio NO tiene asignado un Usuario"""
        member = self.get_by_membership_number(id)
        return member.user == None
    
    


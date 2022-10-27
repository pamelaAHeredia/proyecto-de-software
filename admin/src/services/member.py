import csv, random
from importlib.resources import path
from typing import Optional
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from src.models.database import db
from src.models.club.member import Member
from src.errors import database
from src.services.paginator import Paginator
from src.services.suscription import SuscriptionService
from src.services.movement import MovementService


class MemberService:
    """Clase que representa el manejo de los Socios"""

    _instance = None
    _suscription_service = SuscriptionService()
    _movements_service = MovementService()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemberService, cls).__new__(cls)
        return cls._instance

    def list_members(self):
        """Función que retorna la query de todos los Socios de la Base de Datos ordenada por
        Nro de Socio"""
        return Member.query.order_by(Member.membership_number)

    def list_paginated_members(
        self, page: int, items_per_page: int, endpoint: str, filter: str, search: str
    ) -> Paginator:
        """Función que retorna el paginador con los socios del sistema.

        Args:
           page: Número de pagina.
           items_per_page: cantidad de registros por página.
           endpoint: endpoint para el armado del url_for.

        Returns:
           Un paginador.
        """
        if (not filter or filter == "Todos") and search and search != "":
            members = self.list_by_last_name(substring=search)
        elif (filter) and search and search != "":
            members = self.list_by_last_name(
                substring=search, active=(filter == "Activos")
            )
        elif (not filter or filter == "Todos") and (not search or search == ""):
            members = self.list_members()
        else:
            members = self.list_by_is_active(filter == "Activos")
        return Paginator(members, page, items_per_page, endpoint, filter, search)
    
    def api_get_members(self):
        members = Member.query.filter_by(id=1)
        return self._member_schema.dump(members, many=True)

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
        member = self.find_member(document_type, document_number)
        if not member:
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
            self._suscription_service.associate_member(member)
            return member
        if member.is_active:    
            raise database.ExistingData(
            info="ATENCION!!!",
            message="Ya existe un Socio ACTIVO con ese tipo y numero de documento",)
        else:
            raise database.ExistingData(
            info="ATENCION!!!",
            message="Ya existe un Socio con ese tipo y numero de documento pero INACTIVO",
        )

    def find_member(self, document_type, document_number):
        """Funcion que busca un socio en la base de datos por tipo y numero de documento"""
        return Member.query.filter_by(
            document_type=document_type, document_number=document_number, deleted=False
        ).first()

    def find_member_by_mail(self, email):

        return Member.query.filter_by(email=email, deleted=False).first()

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
        raise database.ExistingData(
            info="ATENCION!!!",
            message="Ya existe el Socio con ese tipo y numero de documento",
        )

    def change_activity_member(self, id):
        """Función que cambia el estado activo/inactivo del Socio"""
        member = self.get_by_membership_number(id)
        if not member.is_active:
            #Podria chequear en este momento si tiene deuda para permitir activar
            member.is_active = True
            self._suscription_service.associate_member(member)
        else:
            member.is_active = False
            for suscription in member.suscriptions:
                if suscription.is_active:
                   self._suscription_service.leave(suscription.id)
            db.session.commit()       
        return member


    def list_by_last_name(self, substring, active: Optional[bool] = None):
        """Función que retorna la lista de todos los Socios que en su apellido tenga
        el substring enviado por parametro"""
        if active is not None:
            return Member.query.filter(
                Member.last_name.ilike("%" + substring + "%"),
                Member.is_active == active,
            ).order_by(Member.membership_number)
        return Member.query.filter(
            Member.last_name.ilike("%" + substring + "%")
        ).order_by(Member.membership_number)

    def list_by_is_active(self, active):
        """Función que retorna la lista de todos los Socios activos o inactivos
        segun el parametro enviado"""
        return Member.query.filter_by(is_active=active).order_by(
            Member.membership_number
        )

    def list_active_and_no_user(self):
        """Función que retorna la lista de todos los Socios activos que no tengan Usuario
        asignado"""
        return Member.query.filter_by(is_active=True, user=None).order_by(
            Member.membership_number
        )

    def format_pdf(self, pdf):
        """Función que define el formato de las paginas del pdf"""
        pdf.drawImage(
            "../admin/src/web/public/logoclub.jpg", 5, 790, width=50, height=50
        )
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
        pdf.drawString(490, 820, "Fecha: " + date.today().strftime("%d/%m/%Y"))
        pdf.drawString(520, 10, "Página " + str(pdf.getPageNumber()))
        return pdf

    def export_list_to_pdf(self, members, line_per_page):
        """Funcion que exporta una lista de Socios a un archivo report.pdf"""
        filename = "src/web/public/report" + str(random.randint(0, 99999)) + ".pdf"
        pdf = canvas.Canvas(filename, pagesize=A4)
        pdf.setTitle("Reporte de Socios")
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

    def export_list_to_csv(self, members):
        """Funcion que exporta una lista de Socios a un archivo report.csv"""
        filename = "src/web/public/report" + str(random.randint(0, 99999)) + ".csv"
        file = open(filename, "w", newline="")
        fields = [
            "N° de Socio",
            "Nombre",
            "Apellido",
            "Tipo de Documento",
            "N° de Documento",
        ]
        salida = csv.DictWriter(file, fieldnames=fields)
        salida.writeheader()
        for member in members:
            salida.writerow(
                {
                    "N° de Socio": member.membership_number,
                    "Nombre": member.first_name,
                    "Apellido": member.last_name,
                    "Tipo de Documento": member.document_type,
                    "N° de Documento": member.document_number,
                }
            )
        file.close()
        return file

    def link_management(self, id_member, id_user):
        """Funcion que vincula un socio con un usuario para ser gestionado"""
        member = self.get_by_membership_number(id_member)
        member.user_id = id_user
        db.session.commit()
        return member

    def unlink_management(self, id_member):
        """Funcion que desvincula un socio del usuario que lo gestiona"""
        member = self.get_by_membership_number(id_member)
        member.user_id = None
        db.session.commit()
        return member

    def members_for_export(self, filter_by_status, filter_by_last_name):

        if filter_by_status == "Todos":
            if filter_by_last_name != "":
                members = self.list_by_last_name(substring=filter_by_last_name)
            else:
                members = self.list_members()
        else:
            if filter_by_last_name != "":
                members = members = self.list_by_last_name(
                    substring=filter_by_last_name,
                    active=(filter_by_status == "Activos"),
                )
            else:
                members = members = self.list_by_is_active(
                    filter_by_status == "Activos"
                )
        return list(members)

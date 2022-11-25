import csv, random, base64, os, uuid
from pathlib import Path
import qrcode
from typing import Optional, List
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import green, red
from reportlab.lib.utils import ImageReader

from src.models.database import db
from src.models.club.member import Member
from src.models.club.member import Picture
from src.models.auth.user import User
from src.errors import database
from src.services.paginator import Paginator
from src.services.suscription import SuscriptionService
from src.services.movement import MovementService
from flask import session, current_app


class MemberService:
    """Clase que representa el manejo de los Socios"""

    _instance = None
    _suscription_service = SuscriptionService()
    _movements_service = MovementService()
    _static_folder = Path(__file__).parents[2].absolute().joinpath("public")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemberService, cls).__new__(cls)
        return cls._instance

    def list_members(self) -> List[Member]:

        """Retorna todos las socios cargadas en la Base de Datos.

        Returns:
            List[Member]: Una lista con todas las disciplinas
        """
        return Member.query.order_by(Member.membership_number)

    def list_paginated_members(
        self,
        page: int,
        items_per_page: int,
        endpoint: str,
        filter: str,
        search: str,
        uniqueCase=False,
    ) -> Paginator:
        """Función que retorna el paginador con los socios del sistema.

        Args:
           page: Número de pagina.
           items_per_page: cantidad de registros por página.
           endpoint: endpoint para el armado del url_for.
           filter: define que tipo de filtro aplicar (Activos-Inactivos-Todos)
           search: string que utiliza para buscar por Apellido

        Returns:
           Un paginador.
        """
        if uniqueCase == True:
            id_user = session["user"]
            members = self.list_by_id_user(id_user=id_user)
            print("Entro")
            for member in members:
                print(member.first_name)
        else:
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
    ) -> Member:

        """Crea un Socio.

        Método que instancia un Socio, lo agrega a la Base de Datos y lo retorna

        Args:
            first_name (str): Nombre del Socio.
            last_name (str): Apellido del Socio.
            document_type (str): Tipo de documento del Socio.
            document_number (str): N° de documento del Socio.
            gender (str): Género del Socio.
            address (str): Domicilio del Socio.
            phone_number (str): N° de Telefono del Socio.Es opcional.
            email (str): Correo electrónico del Socio.Es opcional.

        Raises:
            database.ExistingData: El Socio ya existe.

        Returns:
            Member: Un Socio.
        """
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
                message="Ya existe un Socio ACTIVO con ese tipo y numero de documento",
            )
        else:
            raise database.ExistingData(
                info="ATENCION!!!",
                message="Ya existe un Socio con ese tipo y numero de documento pero INACTIVO",
            )

    def find_member(self, document_type, document_number):
        """Función que busca un Socio por su tipo y N° de documento.

        Args:
           document_type (str): Tipo de documento del Socio.
           document_number (str): N° de documento del Socio.

        Returns:
           Un Member si lo encuentra o None si no lo encuentra.
        """
        return Member.query.filter_by(
            document_type=document_type, document_number=document_number, deleted=False
        ).first()

    def find_member_by_mail(self, email):
        """Función que busca un Socio por su email.

        Args:
            email (str): Correo electrónico del Socio.

        Returns:
           Un Member si lo encuentra o None si no lo encuentra.
        """
        return Member.query.filter_by(email=email, deleted=False).first()

    def get_by_membership_number(self, id) -> Member:
        """Función que retorna un Socio por su N° de Socio.

        Args:
            id (int): N° de Socio

        Returns:
           Un Member
        """
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
        """Actualiza un Socio.

        Método que instancia un Socio, lo actualiza en la Base de Datos y lo guarda.

        Args:
            id (int): N° de Socio
            first_name (str): Nombre del Socio.
            last_name (str): Apellido del Socio.
            document_type (str): Tipo de documento del Socio.
            document_number (str): N° de documento del Socio.
            gender (str): Género del Socio.
            address (str): Domicilio del Socio.
            phone_number (str): N° de Telefono del Socio.Es opcional.
            email (str): Correo electrónico del Socio.Es opcional.

        Raises:
            database.ExistingData: El Socio ya existe.

        Returns:
            Member: Un Socio actualizado.
        """
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

    def change_activity_member(self, id) -> bool:
        """Función que cambia el estado de un Socio de Activo a Inactivo y viceversa.

        Args:
            id (int): N° de Socio

        Returns:
           Un booleano si pudo o no cambiar el estado
        """
        member = self.get_by_membership_number(id)
        change = False
        if not member.is_active:
            if not self._movements_service.is_defaulter(member):
                member.is_active = True
                self._suscription_service.associate_member(member)
                change = True
        else:
            member.is_active = False
            for suscription in member.suscriptions:
                if suscription.is_active:
                    self._suscription_service.leave(suscription.id)
            db.session.commit()
            change = True
        return change

    def list_by_last_name(self, substring, active: Optional[bool] = None):
        """Función que retorna la lista de todos los Socios que en su apellido tenga
        el substring enviado por parametro

        Args:
            substring (String) = Cadena de caracteres a buscar en el campo Apellido del Socio
            active (bool) = Filtro que determina si el Socio es Activo o Inactivo (Opcional)

        Returns:
           Una lista de Socios
        """
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
        segun el parametro enviado

        Args:
            active (bool)= Filtra por Socios Activos(True) o Inactivos(False)

        Returns:
            Una lista de Socios
        """
        return Member.query.filter_by(is_active=active).order_by(
            Member.membership_number
        )

    def list_by_id_user(self, id_user):
        """Función que retorna la lista de todos los Socios asociados a un usuario
        Args:
            id_user (int): id de Usuario

        Returns:
           Una lista de Socios
        """
        return Member.query.filter_by(user_id=id_user).order_by(
            Member.membership_number
        )

    def list_active_and_no_user(self):
        """Función que retorna la lista de todos los Socios activos que no tengan Usuario
        asignado

        Returns:
            Una lista de Socios
        """
        return Member.query.filter_by(is_active=True, user=None).order_by(
            Member.membership_number
        )

    def format_pdf(self, pdf):
        """Función que define el formato de las paginas del pdf

         Args:
            pdf : un pdf(Canvas) para formatear

        Returns:
           Un pdf(Canvas)
        """
        pdf.drawImage("../admin/public/logoclub.jpg", 5, 790, width=50, height=50)
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
        """Funcion que exporta una lista de Socios a un archivo report.pdf

         Args:
            members : Lista de Socios
            line_per_page (int): La cantidad de socios por pagina.

        Returns:
           Un archivo PDF paginado con la lista de Socios recibida
        """
        filename = (
            str(self._static_folder)
            + "/report"
            + str(random.randint(0, 99999))
            + ".pdf"
        )
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

    def no_user(self, id) -> bool:
        """Funcion que retorna True si el Socio NO tiene asignado un Usuario

         Args:
            id (int): N° de Socio

        Returns:
            True si el socio no tiene asignado un Usuario
        """
        member = self.get_by_membership_number(id)
        return member.user == None

    def export_list_to_csv(self, members):
        """Funcion que exporta una lista de Socios a un archivo report.csv

         Args:
            members : Lista de Socios

        Returns:
           Un archivo CSV con la lista de Socios recibida
        """
        filename = (
            str(self._static_folder)
            + "/report"
            + str(random.randint(0, 99999))
            + ".csv"
        )
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
        """Funcion que vincula un socio con un usuario para ser gestionado

         Args:
            id_member (int) : N° de Socio
            id_user (int) : id de Usuario

        Returns:
           Un socio vinculado al usuario.
        """
        member = self.get_by_membership_number(id_member)
        member.user_id = id_user
        db.session.commit()
        return member

    def unlink_management(self, id_member):
        """Funcion que desvincula un socio del usuario que lo gestiona

         Args:
            id_member (int) : N° de Socio

        Returns:
           Un socio sin usuario vinculado.
        """
        member = self.get_by_membership_number(id_member)
        member.user_id = None
        db.session.commit()
        return member

    def members_for_export(self, filter_by_status, filter_by_last_name):
        """Funcion que retorna una lista de Socios a exportar segun los filtros enviados
           por parametro

         Args:
            filter_by_status (string) : Define que filtro aplicar para el estado de actividad del Socio
            filter_by_last_name (string) : Define la busqueda por Apellido del Socio.

        Returns:
            Una lista de Socios filtrada.
        """

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

    def license_to_pdf(self, id_member):
        """Funcion que exporta un Carnet de Socio a un archivo report.pdf

         Args:
            id_member : id de un Socio

        Returns:
           Un archivo PDF con el carnet del Socio del id que viene por argumento
        """
        member = self.get_by_membership_number(id_member)
        filename = (
            str(self._static_folder)
            + "/license"
            + str(random.randint(0, 99999))
            + ".pdf"
        )
        pdf = canvas.Canvas(filename, pagesize=A4)
        pdf.setTitle("Carnet de Socio")
        pdf.drawImage("../admin/public/logoclub2.jpg", 87, 785, width=40, height=40)
        pdf.setFont("Helvetica", 25)
        pdf.setLineWidth(0.2)
        pdf.line(72, 830, 500, 830)
        pdf.line(72, 780, 500, 780)
        pdf.line(72, 560, 500, 560)
        pdf.line(72, 830, 72, 560)
        pdf.line(500, 830, 500, 560)
        pdf.drawCentredString(317, 795, "Club Deportivo Villa Elisa")
        pdf.setFontSize(15)
        pdf.drawCentredString(407, 750, member.first_name + " " + member.last_name)
        pdf.setFontSize(12)
        pdf.drawCentredString(
            407, 730, member.document_type + ": " + member.document_number
        )
        pdf.drawCentredString(407, 710, "Socio: #" + str(member.membership_number))
        pdf.drawCentredString(
            407, 690, "Fecha alta: " + member.creation_date.strftime("%d-%m-%Y %H:%M")
        )
        pdf.setFontSize(15)
        pdf.drawString(177, 620, "Estado:")
        is_defaulter = self._movements_service.is_defaulter(member)
        if is_defaulter:
            pdf.setFillColor(red)
            pdf.drawString(177, 600, "Moroso")
        else:
            pdf.setFillColor(green)
            pdf.drawString(182, 600, "Al dia")
        uuid_name = str(uuid.uuid4())

        picture = member.picture.image
        image_type = member.picture.image_type.replace("image/", "")
        image64 = base64.b64decode(picture)
        img_file_name = os.path.join(self._static_folder, uuid_name + "." + image_type)
        image_result = open(img_file_name, "wb")
        image_result.write(image64)
        image_result.close
        pdf.drawImage(img_file_name, 127, 640, width=130, height=130)

        qr_image = member.picture.qr_image
        qr_image64 = base64.b64decode(qr_image)
        qr_file_name = os.path.join(self._static_folder, f"{uuid_name}_qr.jpg")
        with open(qr_file_name, "wb") as qr_result:
            qr_result.write(qr_image64)
        img = ImageReader(qr_file_name)
        pdf.drawImage(img, 367, 590, width=90, height=90)
        pdf.save()

        os.remove(img_file_name)
        os.remove(qr_file_name)
        return pdf

    def api_members_by_gender(self):
        male = Member.query.filter_by(is_active=True, gender="M").count()
        female = Member.query.filter_by(is_active=True, gender="F").count()
        other = Member.query.filter_by(is_active=True, gender="Otro").count()
        data = {"m": male, "f": female, "otro": other}
        return data

    def api_members_by_activated(self):
        active = Member.query.filter_by(is_active=True).count()
        inactive = Member.query.filter_by(is_active=False).count()
        data = {"active": active, "inactive": inactive}
        return data

    def save_member_photo(self, member, photo_type, photo):
        qr_code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_code.add_data(
            f'{current_app.config["ADMIN_URL"]}/carnet/plantillaCarnet/{member.membership_number}'
        )
        qr_code.make(fit=True)
        qr_img = qr_code.make_image(fill_color="black", back_color="white")
        qr_img_path = os.path.join(
            self._static_folder, f"qr_{member.membership_number}.jpg"
        )
        qr_img.save(qr_img_path)

        with open(qr_img_path, "rb") as img:
            member_qr_image = base64.b64encode(img.read())
            os.remove(qr_img_path)

        member_picture = Picture()
        member_picture.image_type = photo_type
        member_picture.image = photo
        member.picture = member_picture
        member.picture.qr_image = member_qr_image

        try:
            db.session.commit()
        except:
            return False
        return True

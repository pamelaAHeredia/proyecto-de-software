from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.services.settings import SettingsService
from src.services.member import MemberService
from src.services.movement import MovementService
from src.web.forms.setting.forms import SettingsForm
from src.web.forms.setting.mensualPayment import PaymentForm
from src.web.helpers.auth import login_required, is_administrator

import time
settings_blueprint = Blueprint("settings", __name__, url_prefix="/configuraciones")
service = SettingsService()
service_member = MemberService()
service_movement = MovementService()


@settings_blueprint.route("/", methods=["GET", "POST"])
@login_required
@is_administrator
def index():
    """Metodo donde se modifica las configuraciones"""
    form = SettingsForm()
    payment = PaymentForm()

    if (request.method=="GET"):
        settings = service.get_settings()
        form.items_per_page.data = settings.items_per_page
        form.enable_paytable.data = settings.enable_paytable
        form.contact_info.data = settings.contact_info
        form.text_header_payment.data = settings.text_header_payment
        form.amount_monthly.data = settings.amount_monthly
        form.percentage_surcharge.data = settings.percentage_surcharge
    else:
        if form.validate_on_submit():
            print("Entro al form")
            itemsPerPage = form.items_per_page.data
            enablePaytable = form.enable_paytable.data
            contactInfo = form.contact_info.data
            textHeaderPayment = form.text_header_payment.data
            amountMonthly = form.amount_monthly.data
            percentageSurcharge = form.percentage_surcharge.data

            service.load_settings(itemsPerPage=itemsPerPage, 
                                enablePaytable=enablePaytable, 
                                contactInfo=contactInfo, 
                                textHeaderPayment=textHeaderPayment, 
                                amountMonthly=amountMonthly, 
                                percentageSurcharge=percentageSurcharge)
            flash("Configuraciones actualizadas.", "success")
        
        elif payment.validate_on_submit():
            print("Entro al payment")
            month = payment.month.data
            year = payment.year.data
            members = service_member.list_members()
            for member in members:
                if member.is_active:
                    service_movement.generate_mensual_payments(member,month,year)
            flash("Pagos cargados.","success")
            return redirect(url_for("settings.index"))

    return render_template("settings/settings.html",form=form, payment=payment)
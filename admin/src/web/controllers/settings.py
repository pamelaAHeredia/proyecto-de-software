from flask import Blueprint, render_template, request, flash
from src.services.settings import SettingsService
from src.web.forms.setting.forms import SettingsForm
from src.web.helpers.auth import login_required, is_administrator

settings_blueprint = Blueprint("settings", __name__, url_prefix="/configuraciones")
service = SettingsService()


@settings_blueprint.route("/", methods=["GET", "POST"])
@login_required
@is_administrator
def index():

    form = SettingsForm()

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
            itemsPerPage = form.items_per_page.data
            enablePaytable = form.enable_paytable.data
            contactInfo = form.contact_info.data
            textHeaderPayment = form.text_header_payment.data
            amountMonthly = form.amount_monthly.data
            percentageSurcharge = form.percentage_surcharge.data

            service.load_settings(itemsPerPage=itemsPerPage, enablePaytable=enablePaytable, contactInfo=contactInfo, textHeaderPayment=textHeaderPayment, amountMonthly=amountMonthly, percentageSurcharge=percentageSurcharge)
            flash("Configuraciones actualizadas.", "success")

    return render_template("settings/settings.html",form=form)

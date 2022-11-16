from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import session
from services.movement import MovementService

from src.services.settings import SettingsService
from src.services.utils import hash_pass
from src.services.utils import verify_pass
from src.web.helpers.auth import is_member, login_required, verify_permission
from src.services.user import UserService
from src.services.movement import MovementService
from src.services.member import MemberService
from src.web.forms.user import (
    CreateUserForm,
    UpdateUserForm,
    SearchUserForm,
    FilterUsersForm,
    AddRolesForm,
    DeleteRolesForm,
    UnlinkMemberForm,
    UpdatePassForm
)
from src.web.forms.member import FilterSearchForm
from src.errors import database


user_blueprint = Blueprint("users", __name__, url_prefix="/users")

service = UserService()
member_service = MemberService()
settings = SettingsService()
movementService = MovementService()


@user_blueprint.route("/", methods=["GET"])
@login_required
@verify_permission("user_index")
def index():
    filter_form = FilterUsersForm()
    """Render de la lista de usuarios paginada"""
    filter = request.args.get("filter")
    page = request.args.get("page", 1, type=int)
    users_paginator = service.list_paginated_users(
        page, settings.get_items_per_page(), "users.index", filter
    )
    return render_template(
        "users/index.html",
        filter_form=filter_form,
        paginator=users_paginator,
    )


@user_blueprint.route("/filter_users_by", methods=["POST"])
@login_required
@verify_permission("user_search")
def users_filter_by():
    filter_form = FilterUsersForm()

    if filter_form.validate_on_submit:

        page = request.args.get("page", 1, type=int)
        filter = filter_form.filter.data
        users_paginator = service.list_paginated_users(
            page, settings.get_items_per_page(), "users.index", filter
        )
        return render_template(
            "users/index.html",
            paginator=users_paginator,
            filter_form=filter_form,
        )


@user_blueprint.route("/add", methods=["POST", "GET"])
@login_required
@verify_permission("user_create")
def users_add():
    """Agrega usuarios mediante el formulario"""
    form = CreateUserForm()

    if form.validate_on_submit():

        role = service.find_role_by_name(form.roles.data)
        email = form.email.data
        username = form.username.data
        first_name = form.first_name.data
        password = hash_pass(form.email.data)
        last_name = form.last_name.data
        roles = [role]

        try:
            service.create_user(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                roles=roles,
            )
            flash("Usuario creado con éxito!", "success")
        except database.ExistingData as e:
            flash(e, "danger")
    return render_template("users/add_user.html", form=form)


@user_blueprint.route("/update/<id>", methods=["POST", "GET"])
@login_required
@verify_permission("user_update")
def users_update(id):
    form = UpdateUserForm()
    user = service.find_user_by_id(id)

    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            username = form.username.data
            first_name = form.first_name.data
            last_name = form.last_name.data

            try:
                service.update_user(
                    id=id,
                    email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                )
                flash("Usuario actualizado con éxito!", "success")
            except database.ExistingData as e:
                flash(e, "danger")

    return render_template("users/update.html", user=user, form=form)


@user_blueprint.route("/block_user/<id>", methods=["GET"])
@login_required
@verify_permission("user_update")
def users_block(id):
    user = service.find_user_by_id(id)

    try:

        user_session = session["user"]
        service.block_user(id, user_session)
        if user.is_active == False:
            flash("Usuario bloqueado con éxito", "success")
        else:
            flash("Usuario desbloqueado con éxito", "success")
    except database.PermissionDenied as e:
        flash(e, "danger")

    return redirect(url_for("users.index"))


@user_blueprint.route("/search_user", methods=["POST", "GET"])
@login_required
@verify_permission("user_search")
def users_search():
    search_form = SearchUserForm()
    unlink_form = UnlinkMemberForm()

    if request.method == "POST":
        delete_roles_form = DeleteRolesForm()
        add_roles_form = AddRolesForm()

        if search_form.validate_on_submit():
            email = search_form.email.data
            user = service.find_user_byEmail(email)
            return render_template(
                "users/user_info.html",
                user=user,
                add_roles_form=add_roles_form,
                delete_roles_form=delete_roles_form,
                unlink_form=unlink_form
            )
    else:
        return render_template("users/search.html", search_form=search_form)


@user_blueprint.route("/user_info/<id>", methods=["GET", "POST"])
@login_required
@verify_permission("user_show")
def user_info(id):
    delete_roles_form = DeleteRolesForm()
    add_roles_form = AddRolesForm()
    unlink_form = UnlinkMemberForm()

    user = service.find_user_by_id(id)
    return render_template(
        "users/user_info.html",
        user=user,
        add_roles_form=add_roles_form,
        delete_roles_form=delete_roles_form,
        unlink_form=unlink_form,
    )


@user_blueprint.route("/add_roles/<id>", methods=["POST", "GET"])
@login_required
@verify_permission("user_update")
def users_add_roles(id):
    delete_roles_form = DeleteRolesForm()
    add_roles_form = AddRolesForm()
    unlink_form = UnlinkMemberForm()
    user = service.find_user_by_id(id)

    if request.method == "POST":

        if add_roles_form.validate_on_submit:
            role = add_roles_form.roles.data

            try:
                service.add_role(id, role)
                flash("Rol agregado con éxito!", "success")
            except database.ExistingData as e:
                flash(e, "danger")
            except database.PermissionDenied as e:
                flash(e, "danger")
        return render_template(
            "users/user_info.html",
            user=user,
            add_roles_form=add_roles_form,
            delete_roles_form=delete_roles_form,
            unlink_form=unlink_form,
        )
    else:
        return render_template(
            "users/user_info.html",
            user=user,
            add_roles_form=add_roles_form,
            delete_roles_form=delete_roles_form,
            unlink_form=unlink_form,
        )


@user_blueprint.route("/delete_roles/<id>", methods=["POST", "GET"])
@login_required
@verify_permission("user_update")
def users_delete_roles(id):
    delete_roles_form = DeleteRolesForm()
    add_roles_form = AddRolesForm()
    unlink_form = UnlinkMemberForm()
    user = service.find_user_by_id(id)
    roles = service.list_user_roles(id)
    if request.method == "POST":
        if delete_roles_form.validate_on_submit:
            try:
                role = delete_roles_form.role.data
                service.remove_role(id, role)
                flash("Rol eliminado con éxito!", "success")
            except database.PermissionDenied as e:
                flash(e, "danger")
    return render_template(
        "users/user_info.html",
        user=user,
        roles=roles,
        delete_roles_form=delete_roles_form,
        add_roles_form=add_roles_form,
        unlink_form=unlink_form,
    )


@user_blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    delete_roles_form = DeleteRolesForm()
    add_roles_form = AddRolesForm()
    unlink_form = UnlinkMemberForm()
    id = session["user"]

    user = service.find_user_by_id(id)
    return render_template(
        "users/profile.html",
        user=user,
        delete_roles_form=delete_roles_form,
        add_roles_form=add_roles_form,
        unlink_form=unlink_form
    )


@user_blueprint.route("/delete/<id>", methods=["GET"])
@login_required
@verify_permission("user_destroy")
def delete(id):
    filter_form = FilterUsersForm()
    session_id = session["user"]

    try:
        service.delete(id, session_id)
        flash("Usuario eliminado con éxito!", "success")
    except database.PermissionDenied as e:
        flash(e, "danger")
    users = service.list_users()
    return render_template("users/index.html", users=users, filter_form=filter_form)


@user_blueprint.route("/estado_societario/", methods=["GET"])
@login_required
@is_member
def memberState():
    filter_form = FilterSearchForm()
    page = request.args.get("page", 1, type=int)
    filter = request.args.get("filter")
    search = request.args.get("search")
    member_paginator = member_service.list_paginated_members(
        page, settings.get_items_per_page(), "users.memberState", filter, search, True
    )
    return render_template(
        "users/member_state.html", filter_form=filter_form, paginator=member_paginator
    )

@user_blueprint.route("/lista_movimientos/<member_id>", methods=["GET"])
@login_required
def viewMovements(member_id):
    member = member_service.get_by_membership_number(member_id)
    balance = movementService.get_balance(member, all=True)
    page = request.args.get("page", 1, type=int)

    paginator = movementService.list_paginated_movements(
        page,
        settings.get_items_per_page(),
        'users.viewMovements',
        member
    )

    return render_template(
        "users/view_movements.html",
        member=member,
        saldo=balance,
        paginator=paginator,
    )


@user_blueprint.route("/link_user/<id>/<user_id>", methods=["POST", "GET"])
@user_blueprint.route("/link_user/<id>", methods=["POST", "GET"])
@verify_permission("user_update")
@login_required
def link_user(id, user_id=None):
    search_form = SearchUserForm()

    user = None
    member = member_service.get_by_membership_number(id)
    if request.method == "POST":

        if search_form.validate_on_submit and user_id == None:
            email = search_form.email.data
            user = service.find_user_byEmail(email)

            if user:
                if service.contains_role("Socio", user.id):
                    if user.is_active:
                        return render_template(
                            "users/link_user.html",
                            search_form=search_form,
                            member=member,
                            user=user,
                        )
                    else:
                        user=None
                        flash(
                            "El usuario que quiere asignar se encuentra bloqueado.",
                            "danger",
                        )
                else:
                    user=None
                    flash(
                        "El usuario que desea asignar no tiene rol de socio.", "danger"
                    )
            else:
                flash("El email no pertenece a un usuario.", "danger")

        if not user_id == None:
            user = service.find_user_by_id(user_id)
            member = member_service.link_management(id, user.id)
            flash("Usuario asignado con éxito", "success")

    return render_template(
        "users/link_user.html", search_form=search_form, member=member, user=user
    )


@user_blueprint.route("/unlink_member/<id>", methods=["GET", "POST"])
@login_required
@verify_permission("user_update")
def unlink_member(id):
    delete_roles_form = DeleteRolesForm()
    add_roles_form = AddRolesForm()
    unlink_form = UnlinkMemberForm()
    user = service.find_user_by_id(id)

    if request.method == "POST":
        if unlink_form.validate_on_submit:
            member = unlink_form.member.data
            member_service.unlink_management(member)
            flash("Socio desvinculado con éxito!", "success")

    return render_template(
        "users/user_info.html",
        user=user,
        add_roles_form=add_roles_form,
        delete_roles_form=delete_roles_form,
        unlink_form=unlink_form,
    )


@user_blueprint.route("/link_members/<id>", methods=["GET", "POST"])
@login_required
@verify_permission("user_update")
def link_members(id):
    user = service.find_user_by_id(id)
    members = member_service.list_active_and_no_user()

    if request.method == "POST":

        delete_roles_form = DeleteRolesForm()
        add_roles_form = AddRolesForm()
        unlink_form = UnlinkMemberForm()

        members = request.form.getlist("selected")

        for member_id in members:
            member = member_service.get_by_membership_number(member_id)
            member_service.link_management(member.membership_number, user.id)

        return render_template(
                "users/user_info.html",
                user=user,
                add_roles_form=add_roles_form,
                delete_roles_form=delete_roles_form,
                unlink_form=unlink_form
            )

    return render_template(
        "users/link_members.html",
        user=user,
        members=members,
    )

@user_blueprint.route("/update_password", methods=["GET","POST"])
@login_required
def update_password(id=None):
    pass_form = UpdatePassForm()
    id = session["user"]
    user = service.find_user_by_id(id)
    if request.method == "POST":
        
        if pass_form.validate_on_submit:
            current = pass_form.current_password.data
            new = pass_form.new_password.data
            confirm = pass_form.confirm_password.data

            if verify_pass(user.password, current):
                if new == confirm: 
                    service.update_password(hash_pass(new), id)
                    flash("Contraseña Actualizada con éxito", "success")
                else: 
                    flash("Las contraseñas no coinciden", "danger")
            else: 
                flash("Las contraseña actual ingresada no pertenece al usuario", "danger")
        
    return render_template( "users/update_password.html", pass_form=pass_form, user=user)




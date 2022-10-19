from logging.config import IDENTIFIER
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import session

from src.services.utils import hash_pass
from src.web.helpers.auth import login_required, verify_permission
from src.services.user import UserService
from src.services.utils import hash_pass
from src.web.forms.user import (
    CreateUserForm,
    UpdateUserForm,
    SearchUserForm,
    FilterUsersForm,
    AddRolesForm,
    DeleteRolesForm,
)
from src.errors import database


user_blueprint = Blueprint("users", __name__, url_prefix="/users")

service = UserService()


@user_blueprint.get("/")
@login_required
def users_index():
    filter_form = FilterUsersForm()
    """Render de la lista de usuarios paginada"""
    page = request.args.get("page", 1, type=int)
    users_paginator = service.list_paginated_users(page, 2, "users.users_index")
    # users = service.list_users()
    return render_template(
        "users/index.html",
        # users=users,
        filter_form=filter_form,
        paginator=users_paginator,
    )


@user_blueprint.route("/filter_users_by", methods=["POST"])
@login_required
def users_filter_by():
    filter_form = FilterUsersForm()
    search_form = SearchUserForm()
    if filter_form.validate_on_submit:
        filter = filter_form.filter.data
        if filter == "activo":
            users = service.find_active_users()
        elif filter == "bloqueado":
            users = service.find_blocked_users()
        else:
            users = service.list_users()
        print(filter)
        return render_template(
            "users/index.html",
            users=users,
            filter_form=filter_form,
            search_form=search_form,
        )


@user_blueprint.route("/add", methods=["POST", "GET"])
@login_required
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
    else:
        return render_template("users/update.html", user=user, form=form)


@user_blueprint.route("/block_user/<id>", methods=["GET"])
@login_required
def users_block(id):

    user = service.find_user_by_id(id)
    try:
        delete_roles_form = DeleteRolesForm()
        add_roles_form = AddRolesForm()
        user_session = session["user"]
        service.block_user(id, user_session)
        if user.blocked == True:
            flash("Usuario bloqueado con éxito", "success")
        else:
            flash("Usuario desbloqueado con éxito", "success")
    except database.PermissionDenied as e:
        flash(e, "danger")
    return render_template(
        "users/user_info.html",
        user=user,
        add_roles_form=add_roles_form,
        delete_roles_form=delete_roles_form,
    )


@user_blueprint.route("/search_user", methods=["POST", "GET"])
@login_required
def users_search():
    search_form = SearchUserForm()
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
            )
    else:
        return render_template("users/search.html", search_form=search_form)





@user_blueprint.route("/user_info/<id>", methods=["GET", "POST"])
@login_required
def user_info(id):
    delete_roles_form = DeleteRolesForm()
    add_roles_form = AddRolesForm()
    user = service.find_user_by_id(id)
    return render_template(
        "users/user_info.html",
        user=user,
        add_roles_form=add_roles_form,
        delete_roles_form=delete_roles_form,
    )


@user_blueprint.route("/add_roles/<id>", methods=["POST", "GET"])
@login_required
def users_add_roles(id):
    delete_roles_form = DeleteRolesForm()
    add_roles_form = AddRolesForm()
    user = service.find_user_by_id(id)
    if request.method == "POST":
        if add_roles_form.validate_on_submit:
            role = add_roles_form.roles.data
            try:
                service.add_role(id, role)
                flash("Rol agregado con éxito!", "success")
            except database.ExistingData as e:
                flash(e, "danger")
        return render_template(
            "users/roles.html",
            user=user,
            add_roles_form=add_roles_form,
            delete_roles_form=delete_roles_form,
        )
    else:
        return render_template(
            "users/roles.html",
            user=user,
            add_roles_form=add_roles_form,
            delete_roles_form=delete_roles_form,
        )


@user_blueprint.route("/delete_roles/<id>", methods=["POST", "GET"])
@login_required
def users_delete_roles(id):
    delete_roles_form = DeleteRolesForm()
    add_roles_form = AddRolesForm()
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
        "users/roles.html",
        user=user,
        roles=roles,
        delete_roles_form=delete_roles_form,
        add_roles_form=add_roles_form,
    )


@user_blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    delete_roles_form = DeleteRolesForm()
    add_roles_form = AddRolesForm()
    id = session["user"]
    user = service.find_user_by_id(id)
    return render_template(
        "users/profile.html",
        user=user,
        delete_roles_form=delete_roles_form,
        add_roles_form=add_roles_form,
    )


@user_blueprint.route("/delete/<id>", methods=["GET"])
@login_required
@verify_permission("member_destroy")
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

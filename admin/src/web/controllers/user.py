from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import session

from werkzeug.datastructures import MultiDict

from src.services.utils import hash_pass
from src.web.helpers.auth import login_required
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
    search_form = SearchUserForm()
    """Por metodo GET pide la lista total de usuarios al modelo y lo renderiza en la vista"""
    users = service.list_users()
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
        roles = role

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
    delete_roles_form = DeleteRolesForm()
    user = service.find_user_by_id(id)
    try:
        service.block_user(id)
    except database.PermissionDenied as e:
        flash(e, "danger")
    return render_template(
        "users/user_info.html", user=user, delete_roles_form=delete_roles_form
    )


@user_blueprint.route("/search_user", methods=["POST"])
@login_required
def users_search():
    search_form = SearchUserForm()
    delete_roles_form = DeleteRolesForm()
    if search_form.validate_on_submit():
        email = search_form.email.data
        user = service.find_user_byEmail(email)
        return render_template(
            "users/user_info.html",
            user=user,
            search_form=search_form,
            delete_roles_form=delete_roles_form,
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


@user_blueprint.route("/deactivate_user/<id>", methods=["GET"])
@login_required
def users_deactivate(id):
    user = service.find_user_by_id(id)
    service.deactivate_user(id)
    return render_template("users/user_info.html", user=user)


@user_blueprint.route("/add_roles/<id>", methods=["POST", "GET"])
@login_required
def users_add_roles(id):
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
            "users/add_roles.html",
            user=user,
            add_roles_form=add_roles_form,
        )
    else:
        return render_template(
            "users/add_roles.html",
            user=user,
            add_roles_form=add_roles_form,
        )


@user_blueprint.route("/delete_roles/<id>", methods=["POST", "GET"])
@login_required
def users_delete_roles(id):
    delete_roles_form = DeleteRolesForm()
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
    )

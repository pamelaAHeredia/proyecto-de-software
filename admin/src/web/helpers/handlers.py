from flask import render_template

def bad_request(e):
    """Handler de error 400, peticion mala"""
    kwargs = {
        "error_name": "400 Bad Request",
        "error_description": "Se genero un problema en la peticion, revise los datos ingresados",
    }
    return render_template("error.html", **kwargs), 400


def unauthorized(e):
    """Handler de error 401, acceso no autorizado"""
    kwargs = {
        "error_name": "401 Unauthorized",
        "error_description": "Debe iniciar sesión para acceder al recurso",
    }
    return render_template("error.html", **kwargs), 401


def forbidden(e):
    """Handler de error 403, acceso prohibido"""
    kwargs = {
        "error_name": "403 Forbidden",
        "error_description": "Ud. no tiene permisos necesarios para este recurso",
    }
    return render_template("error.html", **kwargs), 403


def not_found_error(e):
    """Handler de error 404, URL no existente"""
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La URL a la que quiere acceder no existe",
    }
    return render_template("error.html", **kwargs), 404


def internal_server_error(e):
    """Handler de error 500, error interno del servidor"""
    kwargs = {
        "error_name": "500 Internal Server Error",
        "error_description": "Error interno del servidor",
    }
    return render_template("error.html", **kwargs), 500

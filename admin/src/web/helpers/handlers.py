from flask import render_template

def not_found_error(e):
    """Handler de error 404"""
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La URL a la que quiere acceder no existe",
    }
    return render_template ("error.html", **kwargs), 404


def internal_server_error(e):
    """Handler de error 500"""
    kwargs = {
        "error_name": "500 Internal Server Error",
        "error_description": "Error interno del servidor",
    }
    return render_template ("error.html", **kwargs), 500
from flask import render_template

def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": " La URL a la que quiere acceder no existe",
    }
    return render_template ("error.html", **kwargs), 404
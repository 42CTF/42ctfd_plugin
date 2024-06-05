import functools

from CTFd.utils.config import ctf_theme
from flask import render_template_string

not_found = """
{% if admin %}
    {% extends "admin/base.html" %}
{% else %}
    {% extends "base.html" %}
{% endif %}

{% block content %}
<div class="container mt-4" style="max-width: 760px">
    <div class="alert alert-warning" role="alert">
        <h4 class="alert-heading">Oops</h4>
        <p>
            It seems you're trying to access a page specific to the
            <strong>42CTF</strong> theme, which is currently inactive.
        </p>
        <p>
            As an admin, you can enable the theme from the 
            <strong>Appearance</strong>/<strong>Theme</strong>
            section in the admin panel.
        </p>
        <hr>
        <p>
            If the theme isn't installed, you can find it on GitHub:
            <a href="https://github.com/42CTF/42ctfd_theme" class="alert-link">
                42CTF Theme
            </a>.
        </p>
    </div>
</div>
{% endblock %}
"""


def ft_theme(admin=False):
    def decorator(f):
        @functools.wraps(f)
        def ft_theme_wrapper(*args, **kwargs):
            if ctf_theme() != "42ctf":
                return render_template_string(not_found, admin=admin)
            return f(*args, **kwargs)

        return ft_theme_wrapper

    return decorator

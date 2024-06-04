import os


def init(app):
    plugin_translations_dir = os.path.join(os.path.dirname(__file__), "translations")
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = ";".join(
        [
            app.config.get("BABEL_TRANSLATION_DIRECTORIES", "translations"),
            plugin_translations_dir,
        ]
    )

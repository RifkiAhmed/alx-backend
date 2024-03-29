#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, g, render_template, request
from flask_babel import Babel
import pytz
from typing import Dict, Optional

app = Flask(__name__)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Class Config"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@app.route("/")
def index() -> str:
    """Render the index page"""
    return render_template("7-index.html")


def get_user() -> Optional[Dict]:
    """Returns the logged-in user based on the login_as parameter"""
    try:
        return users.get(int(request.args.get("login_as")))
    except TypeError:
        return None


@app.before_request
def before_request() -> None:
    """Sets the logged-in user in the global 'g' object"""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """Return the locale received in the requests argument if it's
    supported else retruns the best locale that match the best with
    supported languages
    """
    locale = request.args.get("locale")
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    if g.user and g.user["locale"] in app.config["LANGUAGES"]:
        return g.user["locale"]
    h_locale = request.accept_languages.best_match(app.config["LANGUAGES"])
    if h_locale:
        return h_locale
    return app.config["BABEL_DEFAULT_LOCALE"]


@babel.timezoneselector
def get_timezone() -> str:
    """Returns the appropriate time zone"""
    timezone = None
    if request.args.get("timezone"):
        timezone = request.args.get("timezone")
    elif g.user and g.user["timezone"]:
        timezone = g.user["timezone"]
    try:
        pytz.timezone(timezone)
        return timezone
    except (TypeError, pytz.UnknownTimeZoneError):
        return app.config["BABEL_DEFAULT_TIMEZONE"]


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""

from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

# from application.extensions import (
#     #add as needed
# )


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    register_errorhandlers(app)
    register_blueprints(app)
    return app


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_blueprints(app):
    from application.bank_rate.views import bank_rate
    from application.charities.views import charities
    from application.companies_house.views import companies_house
    from application.elections.views import elections
    from application.frontend.views import frontend
    from application.house_prices.views import house_prices

    app.register_blueprint(frontend)
    app.register_blueprint(house_prices)
    app.register_blueprint(elections)
    app.register_blueprint(bank_rate)
    app.register_blueprint(companies_house)
    app.register_blueprint(charities)


def register_extensions(app):
    pass

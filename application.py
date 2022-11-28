from flask import Flask, Blueprint
from config import *


api = Blueprint('api', __name__, url_prefix=API_PREFIX)

FLASK_CONFIG = os.environ.get('FLASK_CONFIG', 'default')


def init_extensions(app: Flask) -> None:
    """Initialize app extensions"""
    import extensions as ext
    ext.db.init_app(app)
    ext.migrate.init_app(app, ext.db)
    ext.bcrypt.init_app(app)
    ext.ma.init_app(app)
    ext.jwt.init_app(app)


def register_blueprints(app: Flask) -> Flask:
    """Register app blueprints"""
    app.register_blueprint(api)
    return app


def add_cli_commands(app: Flask) -> Flask:
    """Add cli app commands"""
    import cli_commands as cli
    app.cli.add_command(cli.create_db)
    app.cli.add_command(cli.drop_db)
    return app


def create_app(config_mode: str) -> Flask:
    """Flask Application Factory"""

    app = Flask(__name__)

    app.config.from_object(config_by_name[config_mode])

    init_extensions(app)

    app = register_blueprints(app)

    app = add_cli_commands(app)

    return app


from app.views import *  # noqa
from app.models import *  # noqa


app = create_app(config_mode=FLASK_CONFIG)


@app.route("/")
def root():
    return f'This is <b>Notib</b> Project API'


@app.errorhandler(404)
def not_found(error):
    return "Page not found (404)"


if __name__ == "__main__":
    app.run()

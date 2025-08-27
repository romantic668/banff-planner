import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():
    load_dotenv()
    app = Flask(__name__, static_folder="static", template_folder="templates")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///banff.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["OPENWEATHER_API_KEY"] = os.getenv("OPENWEATHER_API_KEY", "")
    app.config["CACHE_TTL_SECONDS"] = int(os.getenv("CACHE_TTL_SECONDS", "600"))

    db.init_app(app)

    from .api import api_bp
    from .pages import pages_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(pages_bp)

    return app

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()

def _resolve_db_uri() -> str:
    """
    优先级：
    1) DATABASE_URL 环境变量（用于你将来切 Postgres 等）
    2) 如果容器里存在 /data（Fly.io 卷的挂载点）→ 用 /data/banff.db
    3) 否则本地开发默认 sqlite:///banff.db
    """
    env_url = os.getenv("DATABASE_URL")
    if env_url:  # 允许传入 sqlite 或 postgres 等
        return env_url

    if os.path.exists("/data"):
        # 绝对路径的 SQLite 要四个斜杠
        return "sqlite:////data/banff.db"

    # 本地开发：项目根目录
    return "sqlite:///banff.db"


def create_app():
    load_dotenv()
    app = Flask(__name__, static_folder="static", template_folder="templates")

    app.config["SQLALCHEMY_DATABASE_URI"] = _resolve_db_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["OPENWEATHER_API_KEY"] = os.getenv("OPENWEATHER_API_KEY", "")
    app.config["CACHE_TTL_SECONDS"] = int(os.getenv("CACHE_TTL_SECONDS", "600"))

    # 如果是 SQLite，给一点更稳的连接参数（多线程/WSGI时更安全）
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:"):
        app.config.setdefault(
            "SQLALCHEMY_ENGINE_OPTIONS",
            {"connect_args": {"check_same_thread": False}}
        )

    db.init_app(app)

    from .api import api_bp
    from .pages import pages_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(pages_bp)

    return app

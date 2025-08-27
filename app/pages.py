from flask import Blueprint, render_template, abort, request
from .models import HikingRoute

pages_bp = Blueprint("pages", __name__)

@pages_bp.get("/")
def index():
    routes = HikingRoute.query.order_by(HikingRoute.id.asc()).all()
    return render_template("index.html", routes=routes)

@pages_bp.get("/route/<int:rid>")
def details(rid: int):
    route = HikingRoute.query.get(rid)
    if not route: abort(404)
    units = request.args.get("units","metric")
    return render_template("details.html", route=route, units=units)

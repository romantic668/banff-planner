from flask import Blueprint, jsonify, request
from .models import HikingRoute
from .services.weather import get_forecast, summarize_daily

api_bp = Blueprint("api", __name__)

@api_bp.get("/routes")
def list_routes():
    rows = HikingRoute.query.order_by(HikingRoute.id.asc()).all()
    return jsonify([r.to_dict() for r in rows])

@api_bp.get("/forecast")
def forecast():
    lat = float(request.args["lat"])
    lon = float(request.args["lon"])
    units = request.args.get("units", "metric")

    raw = get_forecast(lat, lon, units)     # ← 现在返回 onecall 的结构
    daily = summarize_daily(raw, days=3)    # ← 直接读 daily

    return jsonify({"daily": daily, "units": units})


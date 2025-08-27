import time
import requests
from datetime import datetime, timezone
from flask import current_app

_cache = {}

def _key(lat, lon, units):  # 缓存 key：坐标 + 单位
    return f"{lat:.4f},{lon:.4f}:{units}"

def get_forecast(lat: float, lon: float, units: str = "metric"):
    """
    调用 OpenWeather One Call API 3.0：
    https://api.openweathermap.org/data/3.0/onecall
    返回包含 current/hourly/daily（我们会用 daily）
    """
    ttl = int(current_app.config.get("CACHE_TTL_SECONDS", 600))
    k = _key(lat, lon, units)
    now = time.time()

    # 命中缓存且未过期
    if k in _cache and (now - _cache[k][0] < ttl):
        return _cache[k][1]

    api_key = current_app.config.get("OPENWEATHER_API_KEY")
    if not api_key:
        # 没 key → 让前端显示“不可用”
        return None

    url = "https://api.openweathermap.org/data/3.0/onecall"
    # 你可以按需调整 exclude：目前保留 hourly，排除 minutely/alerts
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": units,  # 'metric' | 'imperial' | 'standard'
        "exclude": "minutely,alerts"
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    _cache[k] = (now, data)  # 写缓存
    return data

def _to_iso_date(ts: int) -> str:
    """把秒级时间戳转成 YYYY-MM-DD（UTC）"""
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")

def summarize_daily(data: dict, days: int = 3):
    """
    直接使用 One Call 3.0 的 daily 列表。
    期望输出：[{"date","min","max","desc"} ...]
    """
    if not data:
        return []

    daily = data.get("daily", [])
    if not daily:
        return []

    res = []
    for d in daily[:days]:
        temps = d.get("temp", {})
        weather = (d.get("weather") or [{}])[0]
        res.append({
            "date": _to_iso_date(d.get("dt", 0)),
            "min": round(float(temps.get("min", 0.0)), 1),
            "max": round(float(temps.get("max", 0.0)), 1),
            "desc": weather.get("description", "")
        })
    return res

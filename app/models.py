from . import db

class HikingRoute(db.Model):
    __tablename__ = "hiking_routes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.String(40), nullable=False)
    distance_km = db.Column(db.Float, nullable=False)
    duration_hours = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300), nullable=True)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "difficulty": self.difficulty,
            "distance_km": self.distance_km, "duration_hours": self.duration_hours,
            "lat": self.lat, "lon": self.lon, "image_url": self.image_url or "",
            "description": self.description or ""
        }

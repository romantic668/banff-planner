from app import create_app, db
from app.models import HikingRoute

app = create_app()

with app.app_context():
    db.create_all()  # 确保表存在

    # 1) 清空这张表的所有记录
    db.session.query(HikingRoute).delete()
    db.session.commit()

    # 2) 重新插入英文种子（**不再用 if not ...**）
    seed = [
        ("Lake Agnes Tea House","Easy-Moderate",7.0,2.5,51.4167,-116.2170,"Classic beginner trail, scenic lake and tea house"),
        ("Plain of Six Glaciers","Moderate",13.8,4.5,51.4166,-116.2533,"Panoramic glacier views along the trail"),
        ("Johnston Canyon to Ink Pots","Easy-Moderate",11.7,3.5,51.2457,-115.8395,"Waterfalls plus colorful mineral springs"),
        ("Sulphur Mountain Trail","Moderate",10.1,3.0,51.1486,-115.5719,"Same mountain as the gondola, steady hiking path"),
        ("Moraine Lake Lakeshore","Easy",5.0,1.5,51.3217,-116.1860,"Iconic photo spot of the Valley of the Ten Peaks")
    ]
    for i, s in enumerate(seed, 1):
        db.session.add(HikingRoute(
            id=i, name=s[0], difficulty=s[1], distance_km=s[2], duration_hours=s[3],
            lat=s[4], lon=s[5], image_url=f"https://picsum.photos/seed/{i}/800/400",
            description=s[6]
        ))
    db.session.commit()
    print("HikingRoute reseeded in English.")

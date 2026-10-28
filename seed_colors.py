import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))
from app.main import create_app, db, Color

app = create_app()
with app.app_context():
    # چک کردن رنگ‌های فعلی
    existing = Color.query.all()
    print(f"تعداد رنگ‌های موجود: {len(existing)}")
    for c in existing:
        print(f"  - {c.name}: {c.color_code}")

    # اگر هیچ رنگی نبود، چند رنگ پیش‌فرض اضافه کن
    if len(existing) == 0:
        default_colors = [
            ('قرمز', '#ef4444'),
            ('آبی', '#3b82f6'),
            ('سبز', '#10b981'),
            ('زرد', '#eab308'),
            ('مشکی', '#000000'),
            ('سفید', '#ffffff')
        ]
        for name, code in default_colors:
            db.session.add(Color(name=name, color_code=code))
        db.session.commit()
        print("✅ ۶ رنگ پیش‌فرض اضافه شد")

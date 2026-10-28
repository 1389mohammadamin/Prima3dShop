import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.main import create_app, db, Color

app = create_app()
with app.app_context():
    # ۱. بررسی تعداد رنگ‌ها
    colors = Color.query.all()
    print(f"🔍 تعداد رنگ‌های موجود در دیتابیس: {len(colors)}")
    for c in colors:
        print(f"   - {c.name} ({c.color_code})")

    # ۲. اگر خالی بود، رنگ‌های پیش‌فرض رو اضافه کن
    if len(colors) == 0:
        print("\n⚠️ دیتابیس خالی است. در حال اضافه کردن رنگ‌های پیش‌فرض...")
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
        print("✅ ۶ رنگ پیش‌فرض با موفقیت اضافه شد!")
    else:
        print("\n✅ رنگ‌ها از قبل در دیتابیس وجود دارند.")

    # ۳. چک کردن اینکه جدول colors واقعاً توی دیتابیس هست
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    if 'colors' in inspector.get_table_names():
        print("✅ جدول colors در دیتابیس وجود دارد.")
    else:
        print("❌ جدول colors در دیتابیس وجود ندارد!")

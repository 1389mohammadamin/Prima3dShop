import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.main import create_app, db, Color

app = create_app()
with app.app_context():
    # رنگ‌هایی که می‌خوایم داشته باشیم
    default_colors = [
        ('قرمز', '#ef4444'),
        ('آبی', '#3b82f6'),
        ('مشکی', '#000000'),
        ('سفید', '#ffffff'),
        ('زرد', '#eab308'),
        ('نارنجی', '#f97316'),
        ('بنفش', '#8b5cf6'),
        ('صورتی', '#ec4899')
    ]
    
    for name, code in default_colors:
        # چک میکنیم اگه رنگ از قبل نیست، اضافه بشه
        existing = Color.query.filter_by(name=name).first()
        if not existing:
            db.session.add(Color(name=name, color_code=code))
    
    db.session.commit()
    print("✅ رنگ‌ها با موفقیت به دیتابیس اضافه شدند!")
    
    # نمایش لیست رنگ‌ها
    all_colors = Color.query.all()
    print(f"\n📋 لیست رنگ‌های فعلی ({len(all_colors)} رنگ):")
    for c in all_colors:
        print(f"   - {c.name} ({c.color_code})")

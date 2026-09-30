import os, sys, glob

# پیدا کردن فایل دیتابیس
db_files = glob.glob('**/*.db', recursive=True) + glob.glob('*.db')
print("📁 فایل‌های دیتابیس پیدا شده:")
for f in db_files:
    print(f"   - {f}")

# حذف فایل‌های دیتابیس
for f in db_files:
    try:
        os.remove(f)
        print(f"✅ حذف شد: {f}")
    except Exception as e:
        print(f"❌ خطا در حذف {f}: {e}")

print("\n🔄 حالا دیتابیس رو از نو می‌سازیم...")

# اضافه کردن مسیر پروژه
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("✅ دیتابیس جدید با تمام ستون‌ها ساخته شد")

# manage_db.py
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# اضافه کردن مسیر پروژه
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import create_app
from flask_migrate import Migrate, upgrade, migrate, init, stamp
from config.database import db

app = create_app()
migrate_obj = Migrate(app, db)  # تغییر نام به migrate_obj

def run_migrations():
    """اجرای تمام مراحل مهاجرت"""
    with app.app_context():
        print("📦 در حال آماده‌سازی مهاجرت...")
        
        # اطمینان از وجود پوشه migrations
        if not os.path.exists('migrations'):
            print("🔧 ایجاد پوشه migrations...")
            init(directory='migrations')
            print("✅ پوشه migrations ایجاد شد.")
        
        # ایجاد فایل مهاجرت جدید
        print("📝 ایجاد فایل مهاجرت...")
        from flask_migrate import migrate as flask_migrate
        flask_migrate(directory='migrations', message="Initial migration")
        print("✅ فایل مهاجرت ایجاد شد.")
        
        # اجرای مهاجرت
        print("⬆️ اجرای مهاجرت روی دیتابیس...")
        upgrade(directory='migrations')
        print("✅ مهاجرت با موفقیت اعمال شد!")

if __name__ == "__main__":
    run_migrations()
    print("\n🎉 دیتابیس با موفقیت آماده شد!")
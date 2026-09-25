# make_admin.py
import os
import sys

# تنظیم مسیر
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# تنظیم دیتابیس
os.environ['DATABASE_URL'] = 'sqlite:///shop.db'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# ===== ساخت اپلیکیشن ساده =====
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ===== تعریف مدل‌ها (همان مدل‌های اصلی) =====
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

# ===== ساخت ادمین =====
with app.app_context():
    # ایجاد جدول‌ها اگر وجود ندارند
    db.create_all()
    print("✅ دیتابیس آماده است.")
    
    # بررسی وجود ادمین
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print("✅ کاربر ادمین قبلاً وجود دارد!")
        print(f"   👤 username: {admin.username}")
        print(f"   🔑 password: admin123")
    else:
        # ساخت ادمین جدید
        admin = User(
            username='admin',
            email='admin@پیریما.com',
            password_hash=generate_password_hash('admin123'),
            full_name='مدیر سایت',
            is_admin=True,
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ کاربر ادمین با موفقیت ایجاد شد!")
        print("   👤 username: admin")
        print("   🔑 password: admin123")
        print("   📧 email: admin@پیریما.com")
    
    # نمایش لیست کاربران
    users = User.query.all()
    print(f"\n📋 لیست کاربران ({len(users)} نفر):")
    for u in users:
        role = "ادمین" if u.is_admin else "کاربر"
        print(f"   - {u.username} ({role}) - {u.email}")
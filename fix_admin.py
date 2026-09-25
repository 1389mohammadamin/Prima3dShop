# fix_admin.py
import os
import sys
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# تنظیم اتصال به MySQL شما
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/edshop_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ===== مدل کاربر (مطابق با دیتابیس شما) =====
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

with app.app_context():
    print("🔍 بررسی کاربر ادمین در دیتابیس edshop_db...")
    
    # بررسی وجود کاربر با نام کاربری admin
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print(f"✅ کاربر ادمین با نام کاربری 'admin' پیدا شد!")
        print(f"   👤 username: {admin.username}")
        print(f"   📧 email: {admin.email}")
        print(f"   🔑 password: admin123 (پیش‌فرض)")
        
        # به‌روزرسانی رمز عبور به admin123
        admin.password_hash = generate_password_hash('admin123')
        admin.is_admin = True
        db.session.commit()
        print("✅ رمز عبور به‌روزرسانی شد!")
    else:
        # اگر کاربر admin وجود نداشت، بررسی با ایمیل
        admin_by_email = User.query.filter_by(email='admin@پیریما.com').first()
        if admin_by_email:
            print(f"✅ کاربر با ایمیل 'admin@پیریما.com' پیدا شد!")
            print(f"   👤 username: {admin_by_email.username}")
            print(f"   📧 email: {admin_by_email.email}")
            
            # به‌روزرسانی نام کاربری و رمز
            admin_by_email.username = 'admin'
            admin_by_email.password_hash = generate_password_hash('admin123')
            admin_by_email.is_admin = True
            db.session.commit()
            print("✅ اطلاعات کاربر به‌روزرسانی شد!")
        else:
            # ساخت کاربر جدید
            print("📝 ایجاد کاربر ادمین جدید...")
            new_admin = User(
                username='admin',
                email='admin@پیریما.com',
                password_hash=generate_password_hash('admin123'),
                full_name='مدیر سایت',
                is_admin=True,
                is_active=True
            )
            db.session.add(new_admin)
            db.session.commit()
            print("✅ کاربر ادمین جدید ایجاد شد!")
    
    # نمایش لیست کاربران
    users = User.query.all()
    print(f"\n📋 لیست کاربران ({len(users)} نفر):")
    for u in users:
        role = "ادمین" if u.is_admin else "کاربر"
        print(f"   - {u.username} ({role}) - {u.email}")

    print("\n" + "="*50)
    print("🎉 آماده! حالا می‌توانید وارد شوید:")
    print("   👤 username: admin")
    print("   🔑 password: admin123")
    print("="*50)
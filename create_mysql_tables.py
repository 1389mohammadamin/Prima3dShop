# create_mysql_tables.py
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# تنظیم اتصال به دیتابیس
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from decimal import Decimal

# ساخت اپلیکیشن ساده
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/پیریما_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ===== مدل‌ها =====
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    material = db.Column(db.String(100))
    is_available = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='published')

# ===== ایجاد جدول‌ها =====
with app.app_context():
    print("🗄️ اتصال به دیتابیس:", app.config['SQLALCHEMY_DATABASE_URI'])
    
    # حذف جدول‌های قبلی (احتیاط!)
    # db.drop_all()
    # print("🗑️ جدول‌های قبلی حذف شدند.")
    
    # ایجاد جدول‌ها
    db.create_all()
    print("✅ جدول‌های دیتابیس ایجاد شدند.")
    
    # ایجاد کاربر ادمین
    admin = User.query.filter_by(username='admin').first()
    if not admin:
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
        print("✅ کاربر ادمین ایجاد شد.")
    else:
        print("ℹ️ کاربر ادمین قبلاً وجود دارد.")
    
    # ایجاد دسته‌بندی‌ها
    categories = [
        ('گلدان', 'goldan', 'گلدان‌های زیبا و متنوع'),
        ('مجسمه', 'mojasame', 'مجسمه‌های هنری و دکوری'),
        ('لوازم تحریر', 'lozeme-tahrir', 'لوازم تحریر و وسایل اداری'),
        ('زیورآلات', 'zivaralat', 'زیورآلات و اکسسوری‌ها'),
    ]
    
    for name, slug, desc in categories:
        cat = Category.query.filter_by(name=name).first()
        if not cat:
            cat = Category(name=name, slug=slug, description=desc)
            db.session.add(cat)
    db.session.commit()
    print("✅ دسته‌بندی‌ها ایجاد شدند.")
    
    # ایجاد محصولات نمونه
    products_data = [
        ('گلدان مدرن', 'goldan-modern', 'گلدان زیبا با طرح هندسی', 250000, 10, 'گلدان', 'PLA'),
        ('مجسمه اسب بالدار', 'asb-baladar', 'مجسمه زیبای اسب بالدار', 450000, 5, 'مجسمه', 'ABS'),
        ('جا قلمی سه‌بعدی', 'ja-ghalami', 'جا قلمی شیک و ارگونومیک', 120000, 20, 'لوازم تحریر', 'PETG'),
    ]
    
    for name, slug, desc, price, qty, cat_name, material in products_data:
        if not Product.query.filter_by(name=name).first():
            cat = Category.query.filter_by(name=cat_name).first()
            if cat:
                product = Product(
                    name=name,
                    slug=slug,
                    description=desc,
                    price=Decimal(str(price)),
                    quantity=qty,
                    category_id=cat.id,
                    user_id=admin.id,
                    material=material,
                    is_available=True,
                    status='published'
                )
                db.session.add(product)
    db.session.commit()
    print("✅ محصولات نمونه ایجاد شدند.")
    
    # خلاصه
    print("\n" + "="*50)
    print("🎉 دیتابیس با موفقیت راه‌اندازی شد!")
    print("="*50)
    print(f"\n📊 آمار:")
    print(f"   👤 کاربران: {User.query.count()}")
    print(f"   📂 دسته‌بندی‌ها: {Category.query.count()}")
    print(f"   📦 محصولات: {Product.query.count()}")
    
    print(f"\n🔑 اطلاعات ورود:")
    print(f"   👤 username: admin")
    print(f"   🔑 password: admin123")
    print("\n🚀 برای اجرای سایت: python run.py")
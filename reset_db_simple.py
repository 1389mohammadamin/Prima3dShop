# reset_db_simple.py
import os
import sys
from werkzeug.security import generate_password_hash
from decimal import Decimal

# حذف دیتابیس قدیمی
if os.path.exists('shop.db'):
    os.remove('shop.db')
    print("🗑️ دیتابیس قدیمی حذف شد.")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# تنظیم دیتابیس
os.environ['DATABASE_URL'] = 'sqlite:///shop.db'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# ساخت اپلیکیشن
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ===== مدل‌ها (بدون created_at) =====
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
    db.create_all()
    print("✅ جدول‌های دیتابیس ایجاد شدند.")
    
    # ایجاد کاربر ادمین
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
    
    # ایجاد دسته‌بندی‌ها
    categories = [
        Category(name='گلدان', slug='goldan', description='گلدان‌های زیبا و متنوع'),
        Category(name='مجسمه', slug='mojasame', description='مجسمه‌های هنری و دکوری'),
        Category(name='لوازم تحریر', slug='lozeme-tahrir', description='لوازم تحریر و وسایل اداری'),
        Category(name='زیورآلات', slug='zivaralat', description='زیورآلات و اکسسوری‌ها'),
    ]
    
    for cat in categories:
        db.session.add(cat)
    db.session.commit()
    print("✅ دسته‌بندی‌ها ایجاد شدند.")
    
    # ایجاد محصولات نمونه
    products = [
        Product(
            name='گلدان مدرن',
            slug='goldan-modern',
            description='گلدان زیبا با طرح هندسی',
            price=Decimal('250000'),
            quantity=10,
            category_id=1,
            user_id=1,
            material='PLA',
            is_available=True,
            status='published'
        ),
        Product(
            name='مجسمه اسب بالدار',
            slug='asb-baladar',
            description='مجسمه زیبای اسب بالدار',
            price=Decimal('450000'),
            quantity=5,
            category_id=2,
            user_id=1,
            material='ABS',
            is_available=True,
            status='published'
        ),
        Product(
            name='جا قلمی سه‌بعدی',
            slug='ja-ghalami',
            description='جا قلمی شیک و ارگونومیک',
            price=Decimal('120000'),
            quantity=20,
            category_id=3,
            user_id=1,
            material='PETG',
            is_available=True,
            status='published'
        ),
    ]
    
    for product in products:
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
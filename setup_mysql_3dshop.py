# setup_mysql_پیریما.py
import os
import sys
from werkzeug.security import generate_password_hash
from decimal import Decimal

print("🚀 شروع راه‌اندازی دیتابیس پیریما_db...")

# ===== تنظیمات دقیق MySQL =====
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',  # رمز شما
    'database': 'پیریما_db'  # اسم دقیق دیتابیس شما
}

print(f"📊 اتصال به MySQL: {DB_CONFIG['user']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")

# ===== اتصال با SQLAlchemy =====
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text, ForeignKey

# ساخت اتصال
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
print(f"🔗 اتصال به: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL, echo=False)
    # تست اتصال
    with engine.connect() as conn:
        print("✅ اتصال به MySQL برقرار شد!")
except Exception as e:
    print(f"❌ خطا در اتصال: {e}")
    print("\n💡 راهنمایی:")
    print("1. مطمئن شوید MySQL در حال اجراست")
    print("2. رمز عبور root را بررسی کنید")
    print("3. دیتابیس پیریما_db وجود دارد")
    sys.exit(1)

Base = declarative_base()

# ===== مدل‌ها (بدون created_at) =====
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    full_name = Column(String(100))
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    material = Column(String(100))
    is_available = Column(Boolean, default=True)
    status = Column(String(20), default='published')

# ===== ایجاد جدول‌ها =====
print("\n📝 ایجاد جدول‌ها در پیریما_db...")

try:
    # حذف جدول‌های قبلی
    Base.metadata.drop_all(engine)
    print("🗑️ جدول‌های قبلی حذف شدند (در صورت وجود).")
    
    # ایجاد جدول‌ها
    Base.metadata.create_all(engine)
    print("✅ جدول‌های جدید ایجاد شدند.")
    
except Exception as e:
    print(f"❌ خطا در ایجاد جدول‌ها: {e}")
    sys.exit(1)

# ===== اضافه کردن داده =====
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

print("\n👤 اضافه کردن کاربر ادمین...")

# بررسی وجود ادمین
admin = session.query(User).filter_by(username='admin').first()
if admin:
    print(f"ℹ️ ادمین قبلاً وجود دارد: {admin.username}")
    admin.password_hash = generate_password_hash('admin123')
    admin.is_admin = True
else:
    admin = User(
        username='admin',
        email='admin@پیریما.com',
        password_hash=generate_password_hash('admin123'),
        full_name='مدیر سایت',
        is_admin=True,
        is_active=True
    )
    session.add(admin)
    print("✅ ادمین جدید ساخته شد.")

session.flush()
admin_id = admin.id

# ===== دسته‌بندی‌ها =====
print("\n📂 اضافه کردن دسته‌بندی‌ها...")
categories_data = [
    ('گلدان', 'goldan', 'گلدان‌های زیبا و متنوع'),
    ('مجسمه', 'mojasame', 'مجسمه‌های هنری و دکوری'),
    ('لوازم تحریر', 'lozeme-tahrir', 'لوازم تحریر و وسایل اداری'),
    ('زیورآلات', 'zivaralat', 'زیورآلات و اکسسوری‌ها'),
]

category_ids = {}
for name, slug, desc in categories_data:
    cat = session.query(Category).filter_by(name=name).first()
    if not cat:
        cat = Category(name=name, slug=slug, description=desc)
        session.add(cat)
        session.flush()
        category_ids[name] = cat.id
        print(f"   ✅ {name}")
    else:
        category_ids[name] = cat.id
        print(f"   ℹ️ {name} (موجود)")

# ===== محصولات نمونه =====
print("\n📦 اضافه کردن محصولات نمونه...")
products_data = [
    ('گلدان مدرن', 'goldan-modern', 'گلدان زیبا با طرح هندسی', 250000, 10, 'گلدان', 'PLA'),
    ('مجسمه اسب بالدار', 'asb-baladar', 'مجسمه زیبای اسب بالدار', 450000, 5, 'مجسمه', 'ABS'),
    ('جا قلمی سه‌بعدی', 'ja-ghalami', 'جا قلمی شیک و ارگونومیک', 120000, 20, 'لوازم تحریر', 'PETG'),
    ('گردنبند طرح گل', 'gardanband-gol', 'گردنبند زیبا با طرح گل', 85000, 15, 'زیورآلات', 'PLA'),
]

for name, slug, desc, price, qty, cat_name, mat in products_data:
    existing = session.query(Product).filter_by(name=name).first()
    if not existing:
        product = Product(
            name=name,
            slug=slug,
            description=desc,
            price=Decimal(str(price)),
            quantity=qty,
            category_id=category_ids.get(cat_name, 1),
            user_id=admin_id,
            material=mat,
            is_available=True,
            status='published'
        )
        session.add(product)
        print(f"   ✅ {name}")
    else:
        print(f"   ℹ️ {name} (موجود)")

# ===== ذخیره =====
try:
    session.commit()
    print("\n💾 تغییرات با موفقیت ذخیره شد.")
except Exception as e:
    session.rollback()
    print(f"❌ خطا در ذخیره: {e}")
    sys.exit(1)

# ===== خلاصه =====
print("\n" + "="*60)
print("🎉 دیتابیس پیریما_db با موفقیت راه‌اندازی شد!")
print("="*60)
print(f"\n📊 آمار نهایی:")
print(f"   👤 کاربران: {session.query(User).count()}")
print(f"   📂 دسته‌بندی‌ها: {session.query(Category).count()}")
print(f"   📦 محصولات: {session.query(Product).count()}")

print(f"\n🔑 اطلاعات ورود به سایت:")
print(f"   🌐 آدرس: http://127.0.0.1:5000/auth/login")
print(f"   👤 نام کاربری: admin")
print(f"   🔑 رمز عبور: admin123")

print(f"\n📋 برای مشاهده جدول‌ها در MySQL Workbench:")
print(f"   USE پیریما_db;")
print(f"   SHOW TABLES;")
print("="*60)

session.close()
print("\n🚀 حالا سایت را اجرا کنید: python run.py")
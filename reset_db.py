# reset_db.py
import os
import sys
from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# حذف دیتابیس قدیمی
if os.path.exists('shop.db'):
    os.remove('shop.db')
    print("🗑️ دیتابیس قدیمی حذف شد.")

# import و راه‌اندازی
from app.main import app, db, User, Category, Product

with app.app_context():
    # ایجاد جدول‌ها
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
        Category(name='گلدان', slug='goldan', description='گلدان‌های زیبا'),
        Category(name='مجسمه', slug='mojasame', description='مجسمه‌های هنری'),
        Category(name='لوازم تحریر', slug='lozeme-tahrir', description='لوازم تحریر'),
        Category(name='زیورآلات', slug='zivaralat', description='زیورآلات'),
    ]
    
    for cat in categories:
        db.session.add(cat)
    db.session.commit()
    print("✅ دسته‌بندی‌ها ایجاد شدند.")
    
    # ایجاد محصولات نمونه
    from decimal import Decimal
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
    ]
    
    for product in products:
        db.session.add(product)
    db.session.commit()
    print("✅ محصولات نمونه ایجاد شدند.")
    
    print("\n" + "="*50)
    print("🎉 دیتابیس با موفقیت راه‌اندازی شد!")
    print("="*50)
    print("\n🔑 اطلاعات ورود:")
    print("   👤 username: admin")
    print("   🔑 password: admin123")
    print("\n🚀 برای اجرای سایت: python run.py")
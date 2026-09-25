# setup_all.py
import os
import sys
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ایجاد اپلیکیشن
from app.main import create_app
app = create_app()

# وارد کردن db و مدل‌ها
from config.database import db
from app.infrastructure.database.models import User, Category, Product
from werkzeug.security import generate_password_hash

def setup_all():
    with app.app_context():
        print("="*60)
        print("🚀 شروع راه‌اندازی کامل پروژه پیریما")
        print("="*60)
        
        # 1. ایجاد کاربر ادمین
        print("\n📝 مرحله 1: ایجاد کاربر ادمین")
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
            print("   ✅ کاربر ادمین با موفقیت ایجاد شد!")
            print("   👤 نام کاربری: admin")
            print("   🔑 رمز عبور: admin123")
        else:
            print("   ℹ️ کاربر ادمین قبلاً وجود دارد")
        
        # 2. ایجاد دسته‌بندی‌ها
        print("\n📂 مرحله 2: ایجاد دسته‌بندی‌ها")
        categories = {
            'گلدان': 'گلدان‌های زیبا و متنوع چاپ سه‌بعدی',
            'مجسمه': 'مجسمه‌های هنری و دکوری',
            'لوازم تحریر': 'لوازم تحریر و وسایل اداری',
            'زیورآلات': 'زیورآلات و اکسسوری‌های منحصر‌بفرد',
            'کیت‌های آموزشی': 'کیت‌های آموزشی و علمی',
            'سفارشی': 'محصولات سفارشی بر اساس طرح مشتری'
        }
        
        category_objs = {}
        for name, description in categories.items():
            cat = Category.query.filter_by(name=name).first()
            if not cat:
                cat = Category(
                    name=name,
                    slug=name.replace(' ', '-').lower(),
                    description=description
                )
                db.session.add(cat)
                db.session.commit()
                print(f"   ✅ {name}")
            else:
                print(f"   ℹ️ {name} (موجود)")
            category_objs[name] = cat
        
        # 3. ایجاد محصولات نمونه
        print("\n📦 مرحله 3: ایجاد محصولات نمونه")
        
        products_data = [
            ('گلدان مدرن طرح هندسی', 'گلدان زیبا با طرح هندسی منحصر‌بفرد', 250000, 10, 'گلدان', 'PLA', True),
            ('مجسمه اسب بالدار', 'مجسمه زیبای اسب بالدار با جزئیات کامل', 450000, 5, 'مجسمه', 'ABS', True),
            ('جا قلمی سه‌بعدی ارگونومیک', 'جا قلمی شیک با طراحی ارگونومیک', 120000, 20, 'لوازم تحریر', 'PETG', False),
            ('گردنبند طرح گل رز', 'گردنبند زیبا با طرح گل رز، سبک و منحصر‌بفرد', 85000, 15, 'زیورآلات', 'PLA', False),
            ('کیت آموزشی منظومه شمسی', 'کیت آموزشی شامل ۸ سیاره قابل چاپ', 380000, 8, 'کیت‌های آموزشی', 'PLA', True),
            ('گلدان مینیمال مکعبی', 'گلدان مکعبی با طراحی مینیمال', 180000, 12, 'گلدان', 'PLA', False),
            ('ساعت دیواری مدرن', 'ساعت دیواری با طراحی مدرن و منحصر‌بفرد', 320000, 6, 'لوازم تحریر', 'PLA', True),
        ]
        
        added_count = 0
        for name, desc, price, qty, cat, mat, featured in products_data:
            existing = Product.query.filter_by(name=name).first()
            if not existing:
                product = Product(
                    name=name,
                    slug=name.replace(' ', '-').lower(),
                    description=desc,
                    price=Decimal(str(price)),
                    quantity=qty,
                    category_id=category_objs[cat].id,
                    user_id=admin.id,
                    material=mat,
                    weight=100,
                    print_time=5,
                    is_featured=featured,
                    status='published',
                    is_available=True
                )
                db.session.add(product)
                added_count += 1
                print(f"   ✅ {name}")
            else:
                print(f"   ℹ️ {name} (موجود)")
        
        db.session.commit()
        
        # 4. خلاصه نهایی
        print("\n" + "="*60)
        print("🎉 راه‌اندازی با موفقیت کامل شد!")
        print("="*60)
        print(f"\n📊 آمار نهایی:")
        print(f"   👤 کاربران: {User.query.count()}")
        print(f"   📂 دسته‌بندی‌ها: {Category.query.count()}")
        print(f"   📦 محصولات: {Product.query.count()} ({added_count} جدید)")
        
        print(f"\n🔑 اطلاعات ورود به پنل مدیریت:")
        print(f"   🌐 آدرس: http://127.0.0.1:5000/admin")
        print(f"   👤 نام کاربری: admin")
        print(f"   🔑 رمز عبور: admin123")
        
        print(f"\n🚀 برای اجرای سایت:")
        print(f"   python run.py")
        print("="*60)

if __name__ == "__main__":
    try:
        setup_all()
    except Exception as e:
        print(f"\n❌ خطا: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 راهنمایی:")
        print("1. مطمئن شوید DATABASE_URL در فایل .env درست است")
        print("2. اگر از SQLite استفاده می‌کنید، مسیر فایل را بررسی کنید")
        print("3. اگر از MySQL استفاده می‌کنید، مطمئن شوید سرور روشن است")
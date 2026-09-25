# init_db.py
import os
import sys
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# وارد کردن مستقیم مدل‌ها و db
from config.database import db
from app.infrastructure.database.models import User, Category, Product
from werkzeug.security import generate_password_hash

# ساخت اپلیکیشن و ثبت db
from app.main import create_app
app = create_app()

# مهم: db را با app ثبت کنید
db.init_app(app)

def init_database():
    with app.app_context():
        print("="*60)
        print("🗄️  راه‌اندازی دیتابیس پیریما")
        print("="*60)
        
        # ایجاد جدول‌ها (اگر وجود نداشته باشند)
        print("\n📝 ایجاد جدول‌های دیتابیس...")
        db.create_all()
        print("✅ جدول‌ها با موفقیت ایجاد شدند.")
        
        # 1. ایجاد کاربر ادمین
        print("\n👤 ایجاد کاربر ادمین...")
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
            print("   ✅ کاربر ادمین ایجاد شد!")
            print("   👤 username: admin")
            print("   🔑 password: admin123")
        else:
            print("   ℹ️ کاربر ادمین قبلاً وجود دارد.")
        
        # 2. ایجاد دسته‌بندی‌ها
        print("\n📂 ایجاد دسته‌بندی‌ها...")
        categories = {
            'گلدان': 'گلدان‌های زیبا و متنوع',
            'مجسمه': 'مجسمه‌های هنری و دکوری',
            'لوازم تحریر': 'لوازم تحریر و وسایل اداری',
            'زیورآلات': 'زیورآلات و اکسسوری‌ها',
            'کیت‌های آموزشی': 'کیت‌های آموزشی و علمی',
            'سفارشی': 'محصولات سفارشی'
        }
        
        category_objs = {}
        for name, desc in categories.items():
            cat = Category.query.filter_by(name=name).first()
            if not cat:
                cat = Category(
                    name=name,
                    slug=name.replace(' ', '-').lower(),
                    description=desc
                )
                db.session.add(cat)
                db.session.commit()
                print(f"   ✅ {name}")
            else:
                print(f"   ℹ️ {name} (موجود)")
            category_objs[name] = cat
        
        # 3. ایجاد محصولات نمونه
        print("\n📦 ایجاد محصولات نمونه...")
        products = [
            ('گلدان مدرن طرح هندسی', 'گلدان زیبا با طرح هندسی منحصر‌بفرد', 250000, 10, 'گلدان', 'PLA', True),
            ('مجسمه اسب بالدار', 'مجسمه زیبای اسب بالدار با جزئیات کامل', 450000, 5, 'مجسمه', 'ABS', True),
            ('جا قلمی سه‌بعدی', 'جا قلمی شیک و ارگونومیک', 120000, 20, 'لوازم تحریر', 'PETG', False),
            ('گردنبند طرح گل رز', 'گردنبند زیبا و منحصر‌بفرد', 85000, 15, 'زیورآلات', 'PLA', False),
            ('کیت آموزشی منظومه شمسی', 'کیت آموزشی ۸ سیاره قابل چاپ', 380000, 8, 'کیت‌های آموزشی', 'PLA', True),
        ]
        
        added = 0
        for name, desc, price, qty, cat, mat, featured in products:
            if not Product.query.filter_by(name=name).first():
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
                added += 1
                print(f"   ✅ {name}")
            else:
                print(f"   ℹ️ {name} (موجود)")
        
        db.session.commit()
        
        # خلاصه نهایی
        print("\n" + "="*60)
        print("🎉 راه‌اندازی با موفقیت کامل شد!")
        print("="*60)
        print(f"\n📊 آمار نهایی:")
        print(f"   👤 کاربران: {User.query.count()}")
        print(f"   📂 دسته‌بندی‌ها: {Category.query.count()}")
        print(f"   📦 محصولات: {Product.query.count()} ({added} جدید)")
        
        print(f"\n🔑 اطلاعات ورود:")
        print(f"   🌐 آدرس: http://127.0.0.1:5000")
        print(f"   👤 نام کاربری: admin")
        print(f"   🔑 رمز عبور: admin123")
        
        print(f"\n🚀 برای اجرای سایت:")
        print(f"   python run.py")
        print("="*60)

if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ خطا: {e}")
        import traceback
        traceback.print_exc()
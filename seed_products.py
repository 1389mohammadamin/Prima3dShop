# seed_products.py
import os
import sys
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import create_app
app = create_app()

from config.database import db
from app.infrastructure.database.models import User, Category, Product

def seed_products():
    with app.app_context():
        print("🌱 شروع افزودن محصولات نمونه...")
        
        # پیدا کردن کاربر ادمین
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("❌ کاربر ادمین پیدا نشد! ابتدا create_admin.py را اجرا کنید.")
            return
        
        print(f"✅ کاربر ادمین پیدا شد: {admin.username}")
        
        # ساخت دسته‌بندی‌ها
        categories_data = {
            'گلدان': 'گلدان‌های زیبا و متنوع چاپ سه‌بعدی',
            'مجسمه': 'مجسمه‌های هنری و دکوری',
            'لوازم تحریر': 'لوازم تحریر و وسایل اداری',
            'زیورآلات': 'زیورآلات و اکسسوری‌های منحصر‌بفرد',
            'کیت‌های آموزشی': 'کیت‌های آموزشی و علمی',
            'سفارشی': 'محصولات سفارشی بر اساس طرح مشتری'
        }
        
        category_objs = {}
        for name, description in categories_data.items():
            cat = Category.query.filter_by(name=name).first()
            if not cat:
                cat = Category(
                    name=name,
                    slug=name.replace(' ', '-').lower(),
                    description=description
                )
                db.session.add(cat)
                db.session.commit()
                print(f"✅ دسته‌بندی '{name}' ایجاد شد.")
            else:
                print(f"ℹ️ دسته‌بندی '{name}' قبلاً وجود دارد.")
            category_objs[name] = cat
        
        # محصولات نمونه
        products_data = [
            {
                'name': 'گلدان مدرن طرح هندسی',
                'description': 'گلدان زیبا با طرح هندسی منحصر‌بفرد، مناسب برای دکوراسیون مدرن منزل یا محل کار',
                'price': 250000,
                'quantity': 10,
                'category': 'گلدان',
                'material': 'PLA',
                'weight': 150,
                'print_time': 4,
                'is_featured': True
            },
            {
                'name': 'مجسمه اسب بالدار',
                'description': 'مجسمه زیبای اسب بالدار با جزئیات کامل، تزئینی عالی برای منزل',
                'price': 450000,
                'quantity': 5,
                'category': 'مجسمه',
                'material': 'ABS',
                'weight': 300,
                'print_time': 12,
                'is_featured': True
            },
            {
                'name': 'جا قلمی سه‌بعدی ارگونومیک',
                'description': 'جا قلمی شیک با طراحی ارگونومیک، مناسب برای میز کار و مطالعه',
                'price': 120000,
                'quantity': 20,
                'category': 'لوازم تحریر',
                'material': 'PETG',
                'weight': 80,
                'print_time': 2,
                'is_featured': False
            },
            {
                'name': 'گردنبند طرح گل رز',
                'description': 'گردنبند زیبا با طرح گل رز، سبک و منحصر‌بفرد، هدیه‌ای عالی',
                'price': 85000,
                'quantity': 15,
                'category': 'زیورآلات',
                'material': 'PLA',
                'weight': 20,
                'print_time': 1,
                'is_featured': False
            },
            {
                'name': 'کیت آموزشی منظومه شمسی',
                'description': 'کیت آموزشی شامل ۸ سیاره قابل چاپ، مناسب برای دانش‌آموزان و علاقه‌مندان',
                'price': 380000,
                'quantity': 8,
                'category': 'کیت‌های آموزشی',
                'material': 'PLA',
                'weight': 500,
                'print_time': 20,
                'is_featured': True
            },
            {
                'name': 'گلدان مینیمال مکعبی',
                'description': 'گلدان مکعبی با طراحی مینیمال، مناسب برای گیاهان آپارتمانی',
                'price': 180000,
                'quantity': 12,
                'category': 'گلدان',
                'material': 'PLA',
                'weight': 120,
                'print_time': 3,
                'is_featured': False
            },
            {
                'name': 'ساعت دیواری مدرن',
                'description': 'ساعت دیواری با طراحی مدرن و منحصر‌بفرد، بدون عقربه!',
                'price': 320000,
                'quantity': 6,
                'category': 'لوازم تحریر',
                'material': 'PLA',
                'weight': 200,
                'print_time': 8,
                'is_featured': True
            }
        ]
        
        added_count = 0
        for product_data in products_data:
            # بررسی تکراری نبودن
            existing = Product.query.filter_by(name=product_data['name']).first()
            if existing:
                print(f"ℹ️ محصول '{product_data['name']}' قبلاً وجود دارد.")
                continue
            
            product = Product(
                name=product_data['name'],
                slug=product_data['name'].replace(' ', '-').lower(),
                description=product_data['description'],
                price=Decimal(str(product_data['price'])),
                quantity=product_data['quantity'],
                category_id=category_objs[product_data['category']].id,
                user_id=admin.id,
                material=product_data.get('material', 'PLA'),
                weight=product_data.get('weight', 100),
                print_time=product_data.get('print_time', 5),
                is_featured=product_data.get('is_featured', False),
                status='published',
                is_available=True
            )
            db.session.add(product)
            added_count += 1
            print(f"✅ محصول '{product_data['name']}' ایجاد شد.")
        
        db.session.commit()
        print(f"\n🎉 {added_count} محصول جدید با موفقیت اضافه شدند!")
        print(f"📊 مجموع محصولات: {Product.query.count()}")

if __name__ == "__main__":
    seed_products()
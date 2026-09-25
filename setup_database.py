"""
⭐ راه‌اندازی خودکار دیتابیس
- اگه MySQL در دسترس باشه → استفاده می‌کنه
- اگه MySQL نباشه → SQLite می‌سازه
- روی هاست هم می‌تونه با MySQL کار کنه
"""

import os
import sys

def setup_database():
    print("=" * 60)
    print("🗄️ راه‌اندازی دیتابیس...")
    print("=" * 60)
    
    # =============================================
    # گزینه ۱: استفاده از متغیر محیطی (برای هاست)
    # =============================================
    db_url = os.environ.get('DATABASE_URL', '')
    
    if db_url:
        print(f"✅ دیتابیس از محیط خوانده شد: {db_url[:30]}...")
        return db_url
    
    # =============================================
    # گزینه ۲: تلاش برای اتصال به MySQL
    # =============================================
    try:
        import pymysql
        
        # پسوردها رو اینجا امتحان کن
        passwords = [
            '1234',      # پسورد قبلی
            '',          # بدون پسورد
            'root',      # پسورد root
            'password',  # پسورد پیش‌فرض
        ]
        
        for pwd in passwords:
            try:
                conn = pymysql.connect(
                    host='localhost',
                    user='root',
                    password=pwd,
                    charset='utf8mb4'
                )
                print(f"✅ اتصال به MySQL با پسورد '{pwd}' موفق بود!")
                
                # ساخت دیتابیس
                cursor = conn.cursor()
                cursor.execute('CREATE DATABASE IF NOT EXISTS پیریما_db CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci')
                conn.commit()
                print("✅ دیتابیس 'پیریما_db' ساخته شد")
                conn.close()
                
                return f'mysql+pymysql://root:{pwd}@localhost/پیریما_db?charset=utf8mb4'
                
            except Exception as e:
                continue
        
        print("⚠️ MySQL پیدا شد ولی پسوردش مشخص نیست")
        print("   لطفاً پسورد MySQL رو وارد کن:")
        pwd = input("   پسورد root: ").strip()
        
        if pwd:
            try:
                conn = pymysql.connect(
                    host='localhost',
                    user='root',
                    password=pwd,
                    charset='utf8mb4'
                )
                cursor = conn.cursor()
                cursor.execute('CREATE DATABASE IF NOT EXISTS پیریما_db CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci')
                conn.commit()
                conn.close()
                print("✅ دیتابیس ساخته شد!")
                return f'mysql+pymysql://root:{pwd}@localhost/پیریما_db?charset=utf8mb4'
            except Exception as e:
                print(f"❌ خطا: {e}")
    
    except ImportError:
        print("ℹ️ PyMySQL نصب نیست")
    
    # =============================================
    # گزینه ۳: استفاده از SQLite (پیش‌فرض)
    # =============================================
    print("🔵 استفاده از SQLite (دیتابیس محلی)...")
    sqlite_path = os.path.join(os.path.dirname(__file__), 'پیریما.db')
    print(f"   مسیر: {sqlite_path}")
    
    return f'sqlite:///{sqlite_path}'


def update_main_py(db_url):
    """به‌روزرسانی app/main.py با آدرس دیتابیس"""
    main_path = os.path.join(os.path.dirname(__file__), 'app', 'main.py')
    
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # پیدا کردن خط SQLALCHEMY_DATABASE_URI و جایگزینی
    import re
    
    # الگوهای مختلف
    patterns = [
        r"app\.config\['SQLALCHEMY_DATABASE_URI'\]\s*=\s*[^\n]+",
        r'SQLALCHEMY_DATABASE_URI\s*=\s*[^\n]+',
    ]
    
    new_line = f"app.config['SQLALCHEMY_DATABASE_URI'] = '{db_url}'"
    
    replaced = False
    for pattern in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, new_line, content)
            replaced = True
            print(f"✅ آدرس دیتابیس در main.py به‌روزرسانی شد")
            break
    
    if not replaced:
        # اگه پیدا نشد، قبل از db.init_app اضافه کن
        content = content.replace(
            'db.init_app(app)',
            new_line + '\n    db.init_app(app)'
        )
        print("✅ آدرس دیتابیس اضافه شد")
    
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    print("\n🚀 شروع راه‌اندازی...")
    
    # ۱. نصب pymysql اگه نیست
    try:
        import pymysql
    except ImportError:
        print("📦 نصب PyMySQL...")
        os.system(f'"{sys.executable}" -m pip install pymysql')
        import pymysql
    
    # ۲. پیدا کردن آدرس دیتابیس
    db_url = setup_database()
    
    # ۳. به‌روزرسانی main.py
    update_main_py(db_url)
    
    # ۴. ساخت جدول‌ها
    print("\n📦 ساخت جدول‌ها...")
    sys.path.insert(0, os.path.dirname(__file__))
    
    from app.main import app, db
    
    with app.app_context():
        db.create_all()
        print("✅ تمام جدول‌ها ساخته شدند")
        
        # ساخت ادمین پیش‌فرض
        from app.main import User
        from werkzeug.security import generate_password_hash
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@پیریما.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True,
                name='مدیر سایت'
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ ادمین پیش‌فرض ساخته شد")
            print("   نام کاربری: admin")
            print("   رمز عبور: admin123")
        else:
            print("✅ ادمین از قبل وجود دارد")
    
    print("\n" + "=" * 60)
    print("🎉 همه چیز آماده است!")
    print("=" * 60)
    print("\n📝 حالا بزن: python run.py")

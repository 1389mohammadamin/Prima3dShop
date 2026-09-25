import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import create_app, db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # چک کردن وجود ادمین
    admin = User.query.filter_by(username='MohammadAmin').first()
    
    if admin:
        print("ℹ️ ادمین از قبل وجود دارد")
        print(f"   username: {admin.username}")
        print(f"   email: {admin.email}")
    else:
        admin = User(
            username='MohammadAmin',
            email='Prima3dShop@vatanmail.ir',
            password_hash=generate_password_hash('Mohammad1389Amin'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ ادمین ساخته شد!")
        print("   ─────────────────────")
        print("   👤 username: MohammadAmin")
        print("   🔑 password: Mohammad1389Amin")
        print("   ─────────────────────")
    
    # نمایش همه کاربران
    users = User.query.all()
    print(f"\n📋 تعداد کاربران: {len(users)}")
    for u in users:
        admin_tag = "👑 ادمین" if u.is_admin else "👤 کاربر"
        print(f"   - {u.username} | {u.email} | {admin_tag}")

print("\n🎉 حالا بزن: python run.py")

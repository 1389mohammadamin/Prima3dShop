import sqlite3
import glob
import os

# پیدا کردن همه فایل‌های دیتابیس
db_files = glob.glob('**/*.db', recursive=True) + glob.glob('*.db')
print(f"📁 {len(db_files)} دیتابیس پیدا شد")

for db in db_files:
    if not os.path.exists(db):
        continue
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # چک کردن وجود جدول orders
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
        if not cursor.fetchone():
            print(f"⚠️ {db}: جدول orders نداره")
            conn.close()
            continue

        # چک کردن ستون receipt_image
        cursor.execute('PRAGMA table_info(orders)')
        cols = [c[1] for c in cursor.fetchall()]

        if 'receipt_image' not in cols:
            cursor.execute('ALTER TABLE orders ADD COLUMN receipt_image VARCHAR(300)')
            conn.commit()
            print(f"✅ ستون receipt_image به {db} اضافه شد")
        else:
            print(f"✅ ستون receipt_image در {db} از قبل وجود دارد")

        conn.close()
    except Exception as e:
        print(f"❌ خطا در {db}: {e}")

print("\n🎉 تمام!")

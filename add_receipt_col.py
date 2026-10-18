import sqlite3
import glob
import os

dbs = glob.glob('**/*.db', recursive=True) + glob.glob('*.db')
print(f"📁 {len(dbs)} فایل دیتابیس پیدا شد")

for db in dbs:
    if not os.path.exists(db):
        continue
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        # چک کردن جدول orders
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
        if not cur.fetchone():
            print(f"⚠️ {db}: جدول orders نداره")
            conn.close()
            continue

        # چک کردن ستون receipt_image
        cur.execute('PRAGMA table_info(orders)')
        cols = [c[1] for c in cur.fetchall()]

        if 'receipt_image' not in cols:
            cur.execute('ALTER TABLE orders ADD COLUMN receipt_image VARCHAR(300)')
            conn.commit()
            print(f"✅ {db}: ستون receipt_image اضافه شد")
        else:
            print(f"✅ {db}: ستون receipt_image از قبل وجود دارد")

        conn.close()
    except Exception as e:
        print(f"❌ {db}: {e}")

print("\n🎉 تمام!")

import os
import re

# =============================================
# ۱. اطمینان از وجود variant_id در جدول OrderItem
# =============================================
print("🔄 بررسی جدول OrderItem...")
import sqlite3
import glob

for db in glob.glob('**/*.db', recursive=True) + glob.glob('*.db'):
    if not os.path.exists(db): continue
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='order_items'")
        if not cur.fetchone():
            conn.close()
            continue
        cur.execute('PRAGMA table_info(order_items)')
        cols = [c[1] for c in cur.fetchall()]
        if 'variant_id' not in cols:
            cur.execute('ALTER TABLE order_items ADD COLUMN variant_id INTEGER REFERENCES product_variants(id)')
            conn.commit()
            print(f"✅ ستون variant_id به {db} اضافه شد")
        else:
            print(f"✅ ستون variant_id در {db} وجود دارد")
        conn.close()
    except Exception as e:
        print(f"❌ {db}: {e}")

# =============================================
# ۲. فیکس قالب admin/order_detail.html
# =============================================
print("\n🔄 فیکس قالب ادمین...")
admin_order_path = 'app/interfaces/templates/admin/order_detail.html'

with open(admin_order_path, 'r', encoding='utf-8') as f:
    content = f.read()

# پیدا کردن بخش محصولات
old_product_section = '''<p class="font-semibold">{{ item.product_name }}</p>
                <p class="text-sm text-gray-500">{{ item.product_price|format_currency }} × {{ item.quantity }}</p>'''

new_product_section = '''<p class="font-semibold">{{ item.product_name }}</p>
                {% if item.variant_id %}
                    {% set variant = item.variant %}
                    {% if variant %}
                    <div class="flex items-center gap-2 mt-1">
                        <span class="inline-block w-4 h-4 rounded-full border border-gray-300" style="background-color: {{ variant.color_code or '#ccc' }};"></span>
                        <span class="text-xs text-gray-500">رنگ: {{ variant.value }}</span>
                    </div>
                    {% endif %}
                {% endif %}
                <p class="text-sm text-gray-500">{{ item.product_price|format_currency }} × {{ item.quantity }}</p>'''

if old_product_section in content:
    content = content.replace(old_product_section, new_product_section)
    print("✅ نمایش رنگ به قالب ادمین اضافه شد")
else:
    print("⚠️ بخش محصولات با الگوی دقیق پیدا نشد. شاید ساختار کمی فرق داره.")
    # جایگزینی ساده‌تر
    content = content.replace(
        '<p class="font-semibold">{{ item.product_name }}</p>',
        '<p class="font-semibold">{{ item.product_name }}</p>\n                {% if item.variant %}\n                <div class="flex items-center gap-1 mt-1">\n                    <span class="inline-block w-3 h-3 rounded-full border border-gray-300" style="background-color: {{ item.variant.color_code or \'#ccc\' }};"></span>\n                    <span class="text-xs text-gray-500">رنگ: {{ item.variant.value }}</span>\n                </div>\n                {% endif %}'
    )

with open(admin_order_path, 'w', encoding='utf-8') as f:
    f.write(content)

# =============================================
# ۳. فیکس روت checkout برای ذخیره variant_id در OrderItem
# =============================================
print("\n🔄 فیکس روت checkout برای ذخیره variant_id...")
main_path = 'app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    main_content = f.read()

# پیدا کردن بخش ساخت OrderItem
old_orderitem = '''order_item = OrderItem(
                    order_id=order.id,
                    product_id=item['product'].id,
                    variant_id=item['variant']['id'] if item['variant'] else None,
                    product_name=item['product'].name,
                    product_price=Decimal(str(item['final_price'])),
                    quantity=item['quantity'],
                    total_price=Decimal(str(item['item_total']))
                )'''

# چک کن آیا variant_id توی OrderItem هست یا نه
if 'variant_id=item[\'variant\'][\'id\']' in main_content:
    print("✅ variant_id در OrderItem وجود دارد")
else:
    print("⚠️ variant_id در OrderItem نیست - نیاز به بررسی داره")

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(main_content)

print("\n🎉 تمام!")

main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# پیدا کردن مدل ProductVariant
variant_match = re.search(r'(# ===== مدل تنوع محصولات.*?class ProductVariant\(db\.Model\):.*?)(?=\nclass |\n# ===== |\Z)', content, re.DOTALL)

# پیدا کردن مدل OrderItem
orderitem_match = re.search(r'(class OrderItem\(db\.Model\):.*?)(?=\nclass |\Z)', content, re.DOTALL)

if variant_match and orderitem_match:
    variant_code = variant_match.group(1)
    orderitem_code = orderitem_match.group(1)

    # حذف ProductVariant از جای فعلی
    content = content.replace(variant_code, '')

    # اضافه کردن ProductVariant قبل از OrderItem
    content = content.replace(orderitem_code, variant_code + '\n\n' + orderitem_code)

    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ ProductVariant قبل از OrderItem منتقل شد')
else:
    print('❌ یکی از مدل‌ها پیدا نشد')
    print(f'ProductVariant: {"✅" if variant_match else "❌"}')
    print(f'OrderItem: {"✅" if orderitem_match else "❌"}')

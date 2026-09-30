main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# پیدا کردن مدل ProductSpecification
spec_match = re.search(r'(class ProductSpecification\(db\.Model\):.*?)(?=\nclass |\Z)', content, re.DOTALL)

if spec_match:
    spec_code = spec_match.group(1)

    # حذف از جای فعلی
    content = content.replace(spec_code, '')

    # اضافه کردن بعد از ProductVariant
    variant_match = re.search(r'(class ProductVariant\(db\.Model\):.*?)(?=\nclass |\Z)', content, re.DOTALL)
    if variant_match:
        variant_code = variant_match.group(1)
        content = content.replace(variant_code, variant_code + '\n\n' + spec_code)
        print('✅ ProductSpecification بعد از ProductVariant منتقل شد')
    else:
        print('❌ ProductVariant پیدا نشد')

    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print('❌ ProductSpecification پیدا نشد')

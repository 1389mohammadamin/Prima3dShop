main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# پیدا کردن بخش ساخت محصول و اضافه کردن slug
old_code = """            product = Product(
                name=name,
                description=description,
                price=Decimal(str(price)),
                quantity=int(quantity) if quantity else 0,
                category_id=category_id if category_id else None,
                material=material,
                discount_price=Decimal(str(discount_price)) if discount_price else None
            )"""

new_code = """            import re
            # ساخت slug از نام محصول
            slug = re.sub(r'[^\\w\\-]', '-', name.lower()) if name else ''
            slug = slug[:100] if slug else str(len(Product.query.all()) + 1)
            
            product = Product(
                name=name,
                slug=slug,
                description=description,
                price=Decimal(str(price)),
                quantity=int(quantity) if quantity else 0,
                category_id=category_id if category_id else None,
                material=material,
                discount_price=Decimal(str(discount_price)) if discount_price else None
            )"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ ساخت slug اضافه شد')
else:
    print('⚠️ کد مورد نظر پیدا نشد - باید دستی اضافه کنی')

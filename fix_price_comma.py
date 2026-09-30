main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# فیکس ۱: حذف کاما از price و discount_price
content = content.replace(
    "price = request.form.get('price')",
    "price = request.form.get('price', '').replace(',', '')"
)
content = content.replace(
    "discount_price = request.form.get('discount_price')",
    "discount_price = request.form.get('discount_price', '').replace(',', '')"
)

# فیکس ۲: برای روت admin_product_create
content = content.replace(
    "price = request.form.get('price', '').replace(',', '')",
    "price = request.form.get('price', '').replace(',', '').strip()"
)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ فیکس کاما در قیمت انجام شد')

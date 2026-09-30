main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# الگوی تابع add_to_cart فعلی
pattern = r"(@app\.route\('/add-to-cart/<int:product_id>'.*?def add_to_cart\(product_id\):.*?return redirect\(url_for\('cart'\)\))"

new_add_to_cart = '''@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = request.form.get('quantity', 1, type=int)
    variant_id = request.form.get('variant_id', type=int)

    product = db.session.get(Product, product_id)

    if not product:
        flash('محصول مورد نظر یافت نشد!', 'error')
        return redirect(url_for('products'))

    if quantity > product.quantity:
        flash(f'تعداد درخواستی بیشتر از موجودی است! (موجودی: {product.quantity})', 'error')
        return redirect(url_for('product_detail', product_id=product_id))

    cart = session.get('cart', {})

    # کلید سبد: product_id:variant_id
    if variant_id:
        cart_key = f"{product_id}:{variant_id}"
    else:
        cart_key = str(product_id)

    if cart_key in cart:
        cart[cart_key] += quantity
    else:
        cart[cart_key] = quantity

    session['cart'] = cart
    session.modified = True

    flash(f'{product.name} به سبد خرید اضافه شد!', 'success')
    return redirect(url_for('cart'))'''

if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, new_add_to_cart, content, flags=re.DOTALL)
    print('✅ add_to_cart با پشتیبانی از variant_id به‌روزرسانی شد')
else:
    print('❌ تابع add_to_cart پیدا نشد - دستی بررسی کن')

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

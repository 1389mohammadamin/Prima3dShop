main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# پیدا کردن تابع checkout
pattern = r"(@app\.route\('/checkout'.*?def checkout\(\):.*?return render_template\('checkout\.html'.*?\))"

new_checkout = '''@app.route('/checkout')
@login_required
def checkout():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0

    for cart_key, quantity in cart.items():
        try:
            parts = cart_key.split(':')
            product_id = int(parts[0])
            variant_id = int(parts[1]) if len(parts) > 1 else None

            product = Product.query.get(product_id)
            if product:
                variant_info = None
                if variant_id:
                    variant = ProductVariant.query.get(variant_id)
                    if variant:
                        variant_info = {
                            'id': variant.id,
                            'name': variant.name,
                            'value': variant.value,
                            'color_code': variant.color_code,
                            'price_adjustment': float(variant.price_adjustment)
                        }

                final_price = float(product.price)
                if variant_info:
                    final_price += variant_info['price_adjustment']

                item_total = final_price * quantity
                total_price += item_total
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'item_total': item_total,
                    'final_price': final_price,
                    'variant': variant_info
                })
        except Exception as e:
            print(f"❌ خطا: {e}")

    # محاسبه هزینه پست
    shipping_cost = 0
    try:
        from postal_rates import calculate_shipping
        # فعلاً تهران فرض می‌کنیم - بعداً از فرم می‌گیریم
        shipping_cost = calculate_shipping('تهران')
    except:
        shipping_cost = 0

    total_with_shipping = float(total_price) + shipping_cost

    return render_template('checkout.html',
                          cart_items=cart_items,
                          total_price=total_price,
                          shipping_cost=shipping_cost,
                          total_with_shipping=total_with_shipping)'''

if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, new_checkout, content, flags=re.DOTALL)
    print('✅ تابع checkout با پشتیبانی از variant به‌روزرسانی شد')
else:
    print('❌ تابع checkout پیدا نشد - دستی بررسی کن')

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

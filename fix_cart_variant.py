main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# پیدا کردن روت cart
import re

# الگوی تابع cart فعلی
pattern = r"(@app\.route\('/cart'\).*?def cart\(\):.*?return render_template\('cart\.html'.*?\))"

new_cart = '''@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0

    for cart_key, quantity in cart.items():
        try:
            # جدا کردن product_id و variant_id
            parts = cart_key.split(':')
            product_id = int(parts[0])
            variant_id = int(parts[1]) if len(parts) > 1 else None

            product = Product.query.filter_by(id=product_id).first()
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

                # محاسبه قیمت نهایی با تغییر قیمت رنگ
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
            else:
                cart.pop(cart_key, None)
                session['cart'] = cart
                session.modified = True
        except Exception as e:
            print(f"❌ خطا: {e}")

    # تخفیف
    coupon_data = session.get('coupon')
    discount_amount = 0
    coupon_code = None

    if coupon_data:
        discount_amount = coupon_data.get('discount_amount', 0)
        coupon_code = coupon_data.get('code')
        total_price_float = float(total_price)
        if discount_amount > total_price_float:
            discount_amount = total_price_float
            coupon_data['discount_amount'] = discount_amount
            session['coupon'] = coupon_data
            session.modified = True
        total_price = Decimal(str(total_price_float - discount_amount))
    else:
        total_price = Decimal(str(total_price))

    return render_template('cart.html',
                          cart_items=cart_items,
                          total_price=total_price,
                          discount_amount=discount_amount,
                          coupon_code=coupon_code)'''

# جایگزینی
if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, new_cart, content, flags=re.DOTALL)
    print('✅ روت cart با پشتیبانی از رنگ به‌روزرسانی شد')
else:
    print('❌ روت cart پیدا نشد')

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# پیدا کردن کل تابع checkout از اول تا آخر
pattern = r"(@app\.route\('/checkout'.*?)(?=@app\.route|\Z)"

match = re.search(pattern, content, re.DOTALL)

if match:
    # پیدا کردن تابع کامل
    old_func = match.group(1)
    
    # نمایش خطوط مشکل‌دار
    lines = old_func.split('\n')
    print(f"تعداد خطوط تابع checkout: {len(lines)}")
    
    # پیدا کردن خط try اضافی
    for i, line in enumerate(lines):
        if 'try:' in line and i > 0:
            print(f"خط {i}: {line}")
    
    # ساخت تابع جدید کامل
    new_func = '''@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0

    # پردازش آیتم‌های سبد
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
        shipping_cost = calculate_shipping('تهران')
    except:
        shipping_cost = 0

    total_with_shipping = float(total_price) + shipping_cost

    # POST - ثبت سفارش
    if request.method == 'POST':
        try:
            import random
            import string
            order_number = ''.join(random.choices(string.digits, k=10))

            total_amount = 0
            for item in cart_items:
                total_amount += item['item_total']

            # ساخت سفارش
            order = Order(
                order_number=order_number,
                user_id=current_user.id,
                total_amount=Decimal(str(total_amount)),
                shipping_cost=Decimal(str(shipping_cost)),
                status='pending',
                full_name=request.form.get('full_name'),
                phone=request.form.get('phone'),
                address=request.form.get('address'),
                postal_code=request.form.get('postal_code'),
                province=request.form.get('province', 'تهران')
            )
            db.session.add(order)
            db.session.flush()

            # آیتم‌های سفارش
            for item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item['product'].id,
                    variant_id=item['variant']['id'] if item['variant'] else None,
                    quantity=item['quantity'],
                    price=Decimal(str(item['final_price']))
                )
                db.session.add(order_item)

            db.session.commit()

            # خالی کردن سبد
            session['cart'] = {}
            session.modified = True

            flash(f'سفارش {order_number} با موفقیت ثبت شد!', 'success')
            return redirect(url_for('order_detail', order_id=order.id))

        except Exception as e:
            db.session.rollback()
            flash(f'خطا در ثبت سفارش: {str(e)}', 'error')
            return redirect(url_for('checkout'))

    return render_template('checkout.html',
                          cart_items=cart_items,
                          total_price=total_price,
                          shipping_cost=shipping_cost,
                          total_with_shipping=total_with_shipping)

'''
    
    # جایگزینی
    content = content[:match.start()] + new_func + content[match.end():]
    
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('✅ تابع checkout کامل فیکس شد')
else:
    print('❌ تابع checkout پیدا نشد')

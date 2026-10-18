main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# پیدا کردن آخرین ریدایرکت توی checkout
import re

# چک کردن روت payment_page
if 'def payment_page' not in content:
    print('❌ روت payment_page وجود نداره - باید اضافه بشه')
else:
    print('✅ روت payment_page وجود داره')

# چک کردن ریدایرکت checkout
if "return redirect(url_for('payment_page', order_id=order.id))" in content:
    print('✅ checkout به payment_page ریدایرکت میکنه')
elif "return redirect(url_for('order_detail', order_id=order.id))" in content:
    print('⚠️ checkout مستقیم به order_detail میره - باید عوض بشه')
    
    # پیدا کردن آخرین ریدایرکت بعد از commit سفارش
    # فقط توی تابع checkout عوض کن
    checkout_match = re.search(r'def checkout\(\).*?(?=def |\Z)', content, re.DOTALL)
    if checkout_match:
        checkout_code = checkout_match.group(0)
        if "return redirect(url_for('order_detail', order_id=order.id))" in checkout_code:
            new_checkout = checkout_code.replace(
                "return redirect(url_for('order_detail', order_id=order.id))",
                "return redirect(url_for('payment_page', order_id=order.id))"
            )
            content = content.replace(checkout_code, new_checkout)
            print('✅ ریدایرکت checkout به payment_page عوض شد')
        else:
            print('❌ ریدایرکت توی checkout پیدا نشد')
else:
    print('❌ هیچ ریدایرکتی پیدا نشد')

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

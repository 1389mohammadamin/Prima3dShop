main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# فیکس: ریدایرکت confirm_payment به order_detail
content = content.replace(
    "flash('✅ درخواست تأیید پرداخت شما ثبت شد. پس از بررسی، سفارش شما پردازش می‌شود.', 'success')\n    return redirect(url_for('order_detail', order_id=order.id))",
    "flash('✅ درخواست تأیید پرداخت شما ثبت شد. پس از بررسی، سفارش شما پردازش می‌شود.', 'success')\n    return redirect(url_for('order_detail', order_id=order.id))"
)

# اگه ریدایرکت هنوز به payment_page هست، عوضش کن
content = content.replace(
    "return redirect(url_for('payment_page', order_id=order.id))",
    "return redirect(url_for('order_detail', order_id=order.id))"
)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ ریدایرکت به order_detail فیکس شد')

import os

# =============================================
# ۱. حذف بخش آپلود عکس از payment.html
# =============================================
print("🔄 حذف آپلود عکس از payment.html...")

payment_path = 'app/interfaces/templates/payment.html'
with open(payment_path, 'r', encoding='utf-8') as f:
    content = f.read()

# حذف بخش آپلود عکس
import re

# حذف بلوک آپلود
content = re.sub(
    r'<div class="mb-4">\s*<label[^>]*>آپلود تصویر فیش[^<]*</label>.*?</div>',
    '',
    content,
    flags=re.DOTALL
)

# تغییر enctype فرم (دیگه نیازی به آپلود نیست)
content = content.replace(
    'enctype="multipart/form-data"',
    ''
)

with open(payment_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ آپلود عکس از payment.html حذف شد")

# =============================================
# ۲. فیکس نمایش فیش برای سفارش‌های قدیمی
# =============================================
print("\n🔄 فیکس نمایش فیش برای سفارش‌های قدیمی...")

# چک کردن قالب admin/order_detail.html
admin_order_path = 'app/interfaces/templates/admin/order_detail.html'

if os.path.exists(admin_order_path):
    with open(admin_order_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # چک کن بخش فیش وجود داره
    if 'receipt_image' not in content:
        print("⚠️ بخش فیش در admin/order_detail.html وجود نداره")
    else:
        print("✅ بخش فیش در admin/order_detail.html وجود داره")

        # فیکس: استفاده از getattr برای سفارش‌های قدیمی
        content = content.replace(
            '{% if order.receipt_image %}',
            '{% if order.receipt_image is defined and order.receipt_image %}'
        )

        with open(admin_order_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ چک امن برای receipt_image اضافه شد")

# =============================================
# ۳. فیکس روت confirm_payment (حذف آپلود)
# =============================================
print("\n🔄 فیکس روت confirm_payment...")

main_path = 'app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# پیدا کردن تابع confirm_payment
pattern = r"(@app\.route\('/order/<int:order_id>/confirm-payment'.*?def confirm_payment\(order_id\):.*?return redirect\(url_for\('order_detail', order_id=order\.id\)\))"

new_confirm = '''@app.route('/order/<int:order_id>/confirm-payment', methods=['POST'])
@login_required
def confirm_payment(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))

    order.status = 'pending_confirmation'
    db.session.commit()

    flash('✅ درخواست تأیید پرداخت شما ثبت شد. پس از بررسی، سفارش شما پردازش می‌شود.', 'success')
    return redirect(url_for('order_detail', order_id=order.id))'''

if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, new_confirm, content, flags=re.DOTALL)
    print("✅ روت confirm_payment فیکس شد (بدون آپلود)")
else:
    print("❌ روت confirm_payment پیدا نشد")

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n🎉 همه کارها انجام شد!")

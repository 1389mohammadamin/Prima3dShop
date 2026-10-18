import os
import re

# =============================================
# بخش ۱: اضافه کردن فیلد receipt_image به مدل Order
# =============================================
print("🔄 افزودن فیلد receipt_image به مدل Order...")

with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# اضافه کردن فیلد بعد از shipping_cost
if 'receipt_image' not in content:
    content = content.replace(
        "shipping_cost = db.Column(db.Numeric(10, 2), default=0)",
        "shipping_cost = db.Column(db.Numeric(10, 2), default=0)\n    receipt_image = db.Column(db.String(300), nullable=True)"
    )
    print("✅ فیلد receipt_image به مدل Order اضافه شد")
else:
    print("✅ فیلد receipt_image از قبل وجود دارد")

# =============================================
# بخش ۲: فیکس روت confirm_payment برای ذخیره عکس
# =============================================
print("\n🔄 فیکس روت confirm_payment...")

# پیدا کردن تابع confirm_payment
pattern = r"(@app\.route\('/order/<int:order_id>/confirm-payment'.*?def confirm_payment\(order_id\):.*?return redirect\(url_for\('order_detail', order_id=order\.id\)\))"

new_confirm = '''@app.route('/order/<int:order_id>/confirm-payment', methods=['POST'])
@login_required
def confirm_payment(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))

    # ذخیره عکس فیش
    receipt = request.files.get('receipt')
    if receipt and receipt.filename:
        # ساخت پوشه receipts اگه نیست
        receipts_dir = os.path.join('app', 'interfaces', 'static', 'receipts')
        os.makedirs(receipts_dir, exist_ok=True)

        # ساخت اسم فایل یکتا
        import uuid
        ext = os.path.splitext(receipt.filename)[1]
        filename = f"receipt_{order.order_number}_{uuid.uuid4().hex[:8]}{ext}"
        filepath = os.path.join(receipts_dir, filename)
        receipt.save(filepath)
        order.receipt_image = f"/static/receipts/{filename}"
        print(f"✅ عکس ذخیره شد: {filepath}")

    order.status = 'pending_confirmation'
    db.session.commit()

    flash('✅ درخواست تأیید پرداخت شما ثبت شد. پس از بررسی، سفارش شما پردازش می‌شود.', 'success')
    return redirect(url_for('order_detail', order_id=order.id))'''

if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, new_confirm, content, flags=re.DOTALL)
    print("✅ روت confirm_payment فیکس شد")
else:
    print("❌ روت confirm_payment پیدا نشد")

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

# =============================================
# بخش ۳: ساخت روت‌های دانلود و حذف عکس
# =============================================
print("\n🔄 افزودن روت‌های دانلود و حذف عکس...")

with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'def admin_download_receipt' not in content:
    new_routes = '''
# ===== دانلود فیش =====
@app.route('/admin/order/<int:order_id>/receipt/download')
@login_required
def admin_download_receipt(order_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    order = Order.query.get_or_404(order_id)
    if not order.receipt_image:
        flash('فیشی برای این سفارش آپلود نشده!', 'error')
        return redirect(url_for('admin_order_detail', order_id=order_id))
    filepath = os.path.join('app', 'interfaces', order.receipt_image.lstrip('/'))
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    flash('فایل فیش پیدا نشد!', 'error')
    return redirect(url_for('admin_order_detail', order_id=order_id))


# ===== حذف فیش =====
@app.route('/admin/order/<int:order_id>/receipt/delete', methods=['POST'])
@login_required
def admin_delete_receipt(order_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    order = Order.query.get_or_404(order_id)
    if order.receipt_image:
        filepath = os.path.join('app', 'interfaces', order.receipt_image.lstrip('/'))
        if os.path.exists(filepath):
            os.remove(filepath)
        order.receipt_image = None
        db.session.commit()
        flash('✅ فیش با موفقیت حذف شد!', 'success')
    return redirect(url_for('admin_order_detail', order_id=order_id))

'''
    create_app_pos = content.find('def create_app():')
    if create_app_pos > 0:
        content = content[:create_app_pos] + new_routes + '\n' + content[create_app_pos:]
        print("✅ روت‌های دانلود و حذف اضافه شدند")

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

# =============================================
# بخش ۴: اضافه کردن send_file به importها
# =============================================
print("\n🔄 افزودن send_file به importها...")

with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'from flask import' in content and 'send_file' not in content:
    # پیدا کردن خط import flask
    match = re.search(r"from flask import ([^\n]+)", content)
    if match:
        imports = match.group(1)
        if 'send_file' not in imports:
            new_imports = imports + ', send_file'
            content = content.replace(f"from flask import {imports}", f"from flask import {new_imports}")
            print("✅ send_file به importها اضافه شد")

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n🎉 همه کارها انجام شد!")

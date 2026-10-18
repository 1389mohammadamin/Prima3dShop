import os
import re

# =============================================
# بخش ۱: تغییر اسم سایت به پریما استور
# =============================================
print("🔄 تغییر اسم سایت...")

html_files = []
for root, dirs, files in os.walk('app/interfaces/templates'):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = content.replace('پیریما Shop 3D', 'پریما استور')
    content = content.replace('پیریما شاپ', 'پریما استور')
    content = content.replace('پیریما', 'پریما استور')
    content = content.replace('Prima3dShop', 'PrimaStore')
    content = content.replace('Prima 3D Shop', 'پریما استور')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {os.path.basename(filepath)}")

print("✅ اسم سایت تغییر کرد")

# =============================================
# بخش ۲: ساخت قالب صفحه پرداخت
# =============================================
print("\n🔄 ساخت صفحه پرداخت...")

payment_html = '''{% extends "base.html" %}
{% block title %}پرداخت سفارش - پریما استور{% endblock %}
{% block content %}
<div class="max-w-3xl mx-auto">
    <div class="bg-white rounded-2xl shadow-lg p-8">
        <div class="text-center mb-8">
            <div class="inline-flex items-center justify-center w-20 h-20 bg-emerald-100 rounded-full mb-4">
                <i class="fas fa-credit-card text-4xl text-emerald-600"></i>
            </div>
            <h1 class="text-3xl font-bold text-gray-800">پرداخت سفارش</h1>
            <p class="text-gray-500 mt-2">شماره سفارش: <span class="font-bold text-emerald-600">{{ order.order_number }}</span></p>
        </div>

        <!-- مبلغ قابل پرداخت -->
        <div class="bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-xl p-6 text-white text-center mb-8">
            <p class="text-sm opacity-90 mb-2">مبلغ قابل پرداخت</p>
            <p class="text-4xl font-bold">{{ order.total_amount|format_currency }}</p>
        </div>

        <!-- اطلاعات حساب -->
        <div class="bg-gray-50 rounded-xl p-6 mb-8 border-2 border-emerald-200">
            <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
                <i class="fas fa-university text-emerald-600"></i>
                اطلاعات حساب برای واریز
            </h2>

            <div class="space-y-4">
                <!-- شماره حساب -->
                <div class="bg-white rounded-lg p-4 border">
                    <p class="text-sm text-gray-500 mb-1">شماره حساب</p>
                    <div class="flex items-center justify-between gap-3">
                        <p class="text-2xl font-bold text-gray-800 tracking-wider" id="account-number" dir="ltr">6219861862220273</p>
                        <button onclick="copyAccount()" class="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 transition flex items-center gap-2">
                            <i class="fas fa-copy"></i>
                            <span>کپی</span>
                        </button>
                    </div>
                </div>

                <!-- آیدی -->
                <div class="bg-white rounded-lg p-4 border">
                    <p class="text-sm text-gray-500 mb-1">آیدی برای ارسال فیش</p>
                    <div class="flex items-center justify-between gap-3">
                        <p class="text-2xl font-bold text-gray-800" id="account-id" dir="ltr">@prima3dstore</p>
                        <button onclick="copyId()" class="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 transition flex items-center gap-2">
                            <i class="fas fa-copy"></i>
                            <span>کپی</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- راهنما -->
        <div class="bg-amber-50 border-2 border-amber-200 rounded-xl p-6 mb-8">
            <h3 class="font-bold text-amber-800 mb-3 flex items-center gap-2">
                <i class="fas fa-info-circle"></i>
                راهنمای پرداخت
            </h3>
            <ol class="list-decimal list-inside space-y-2 text-gray-700 text-sm">
                <li>مبلغ <strong class="text-emerald-600">{{ order.total_amount|format_currency }}</strong> را به شماره حساب بالا واریز کنید.</li>
                <li>پس از واریز، <strong>عکس فیش پرداخت</strong> را در پیام‌رسان‌های زیر برای ما ارسال کنید.</li>
                <li>حتماً <strong>شماره سفارش ({{ order.order_number }})</strong> را در پیام خود ذکر کنید.</li>
                <li>پس از تأیید، سفارش شما در اسرع وقت پردازش می‌شود.</li>
            </ol>
        </div>

        <!-- دکمه‌های ارسال فیش -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
            <a href="https://ble.ir/prima3dstore" target="_blank"
               class="flex items-center justify-center gap-3 bg-emerald-500 text-white px-6 py-4 rounded-xl hover:bg-emerald-600 transition font-bold text-lg">
                <i class="fas fa-comments text-2xl"></i>
                <span>ارسال فیش در بله</span>
            </a>
            <a href="https://t.me/prima3dstore" target="_blank"
               class="flex items-center justify-center gap-3 bg-sky-500 text-white px-6 py-4 rounded-xl hover:bg-sky-600 transition font-bold text-lg">
                <i class="fab fa-telegram text-2xl"></i>
                <span>ارسال فیش در تلگرام</span>
            </a>
        </div>

        <!-- تأیید پرداخت -->
        <div class="border-t pt-6">
            <form action="/order/{{ order.id }}/confirm-payment" method="POST" enctype="multipart/form-data">
                <input type="hidden" name="order_id" value="{{ order.id }}">
                <div class="mb-4">
                    <label class="block text-sm font-semibold mb-2">آپلود تصویر فیش (اختیاری)</label>
                    <input type="file" name="receipt" accept="image/*"
                           class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-emerald-500">
                </div>
                <button type="submit"
                        class="w-full bg-emerald-600 text-white px-6 py-4 rounded-xl hover:bg-emerald-700 transition font-bold text-lg">
                    <i class="fas fa-check-circle ml-2"></i>
                    پرداخت را انجام دادم
                </button>
            </form>
        </div>

        <div class="mt-4 text-center">
            <a href="/profile" class="text-gray-500 hover:text-emerald-600 text-sm">
                <i class="fas fa-arrow-left ml-1"></i>
                بازگشت به پروفایل
            </a>
        </div>
    </div>
</div>

<script>
    function copyAccount() {
        navigator.clipboard.writeText('6219861862220273');
        alert('✅ شماره حساب کپی شد!');
    }

    function copyId() {
        navigator.clipboard.writeText('prima3dstore');
        alert('✅ آیدی کپی شد!');
    }
</script>
{% endblock %}
'''

with open('app/interfaces/templates/payment.html', 'w', encoding='utf-8') as f:
    f.write(payment_html)

print("✅ صفحه payment.html ساخته شد")

# =============================================
# بخش ۳: اضافه کردن روت صفحه پرداخت به main.py
# =============================================
print("\n🔄 اضافه کردن روت پرداخت...")

with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# چک کن روت وجود داره یا نه
if 'def payment_page' not in content:
    new_route = '''
# ===== صفحه پرداخت =====
@app.route('/order/<int:order_id>/payment')
@login_required
def payment_page(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    return render_template('payment.html', order=order)


# ===== تأیید پرداخت =====
@app.route('/order/<int:order_id>/confirm-payment', methods=['POST'])
@login_required
def confirm_payment(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))

    order.status = 'pending_confirmation'
    db.session.commit()

    flash('✅ درخواست تأیید پرداخت شما ثبت شد. پس از بررسی، سفارش شما پردازش می‌شود.', 'success')
    return redirect(url_for('order_detail', order_id=order.id))

'''

    # اضافه کردن قبل از def create_app
    create_app_pos = content.find('def create_app():')
    if create_app_pos > 0:
        content = content[:create_app_pos] + new_route + '\n' + content[create_app_pos:]
        print("✅ روت‌های پرداخت اضافه شدند")
    else:
        print("❌ create_app پیدا نشد")
else:
    print("✅ روت پرداخت از قبل وجود دارد")

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

# =============================================
# بخش ۴: تغییر ریدایرکت checkout به صفحه پرداخت
# =============================================
print("\n🔄 تغییر ریدایرکت checkout...")

with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# تغییر redirect بعد از ساخت سفارش
content = content.replace(
    "return redirect(url_for('order_detail', order_id=order.id))",
    "return redirect(url_for('payment_page', order_id=order.id))"
)

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ ریدایرکت به صفحه پرداخت تغییر کرد")
print("\n🎉 همه کارها انجام شد!")

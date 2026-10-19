import os
import re

# =============================================
# ۱. بازنویسی کامل coupon_form.html
# =============================================
coupon_form_path = 'app/interfaces/templates/admin/coupon_form.html'

html_content = '''{% extends "base.html" %}

{% block title %}کد تخفیف جدید - پریما استور{% endblock %}

{% block content %}
<div class="max-w-3xl mx-auto bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
    <div class="flex justify-between items-center mb-8 border-b pb-4">
        <h1 class="text-2xl font-bold text-gray-800">ایجاد کد تخفیف جدید</h1>
        <a href="/admin/coupons" class="text-gray-500 hover:text-emerald-600 transition text-sm flex items-center gap-1">
            <i class="fas fa-arrow-right"></i> بازگشت به لیست
        </a>
    </div>

    <form method="POST" action="/admin/coupons/create" class="space-y-6">
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- کد تخفیف -->
            <div>
                <label class="block text-sm font-semibold mb-2 text-gray-700">کد تخفیف *</label>
                <input type="text" name="code" required placeholder="مثلاً: OFF10" dir="ltr"
                       class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition uppercase">
            </div>

            <!-- توضیحات -->
            <div>
                <label class="block text-sm font-semibold mb-2 text-gray-700">توضیحات</label>
                <input type="text" name="description" placeholder="اختیاری"
                       class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition">
            </div>

            <!-- نوع تخفیف -->
            <div>
                <label class="block text-sm font-semibold mb-2 text-gray-700">نوع تخفیف *</label>
                <select name="discount_type" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition">
                    <option value="percent">درصدی</option>
                    <option value="fixed">مبلغ ثابت</option>
                </select>
            </div>

            <!-- مقدار تخفیف -->
            <div>
                <label class="block text-sm font-semibold mb-2 text-gray-700">مقدار تخفیف *</label>
                <input type="number" name="discount_value" required placeholder="مثلاً: 10"
                       class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition" dir="ltr">
            </div>

            <!-- حداقل مبلغ سفارش -->
            <div>
                <label class="block text-sm font-semibold mb-2 text-gray-700">حداقل مبلغ سفارش (تومان)</label>
                <input type="text" name="min_order_amount" value="0" 
                       onkeyup="this.value = this.value.replace(/[^0-9]/g, '').replace(/\\\\B(?=(\\\\d{3})+(?!\\\\d))/g, ',')"
                       class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition" dir="ltr">
            </div>

            <!-- حداکثر تخفیف -->
            <div>
                <label class="block text-sm font-semibold mb-2 text-gray-700">حداکثر تخفیف (اختیاری)</label>
                <input type="text" name="max_discount_amount" placeholder="مثلاً: 500,000"
                       onkeyup="this.value = this.value.replace(/[^0-9]/g, '').replace(/\\\\B(?=(\\\\d{3})+(?!\\\\d))/g, ',')"
                       class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition" dir="ltr">
            </div>

            <!-- تعداد دفعات استفاده -->
            <div>
                <label class="block text-sm font-semibold mb-2 text-gray-700">تعداد دفعات مجاز</label>
                <input type="number" name="usage_limit" value="1" min="1"
                       class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition" dir="ltr">
            </div>

            <!-- تاریخ انقضا -->
            <div>
                <label class="block text-sm font-semibold mb-2 text-gray-700">تاریخ انقضا (اختیاری)</label>
                <input type="date" name="expiry_date"
                       class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition" dir="ltr">
            </div>
        </div>

        <!-- وضعیت -->
        <div class="bg-gray-50 p-5 rounded-xl border border-gray-200">
            <label class="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" name="is_active" value="1" checked class="w-5 h-5 text-emerald-600 rounded focus:ring-emerald-500">
                <span class="text-sm font-bold text-gray-700">فعال باشد</span>
            </label>
        </div>

        <!-- دکمه‌ها -->
        <div class="flex gap-4 pt-6 border-t">
            <button type="submit" class="bg-emerald-600 text-white px-8 py-3 rounded-xl hover:bg-emerald-700 transition font-bold text-lg shadow-md flex-1">
                <i class="fas fa-save ml-2"></i> ذخیره کد تخفیف
            </button>
            <a href="/admin/coupons" class="bg-gray-200 text-gray-700 px-8 py-3 rounded-xl hover:bg-gray-300 transition font-bold text-lg text-center flex items-center justify-center">
                انصراف
            </a>
        </div>
    </form>
</div>
{% endblock %}
'''

with open(coupon_form_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
print("✅ فرم ساخت کد تخفیف بازنویسی شد")

# =============================================
# ۲. بررسی روت admin_coupon_create در main.py
# =============================================
main_path = 'app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# چک کنیم که روت ساخت کوپن درست کار می‌کنه
if 'def admin_coupon_create' not in content:
    print("⚠️ روت admin_coupon_create پیدا نشد!")
else:
    print("✅ روت admin_coupon_create وجود دارد")

print("\n🎉 تمام! حالا سرور رو ریستارت کن.")

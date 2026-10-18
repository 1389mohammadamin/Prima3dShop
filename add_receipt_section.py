import os
import re

admin_order_path = 'app/interfaces/templates/admin/order_detail.html'

if not os.path.exists(admin_order_path):
    print(f"❌ {admin_order_path} پیدا نشد")
else:
    with open(admin_order_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'receipt_image' in content:
        print("✅ بخش فیش از قبل وجود دارد")
    else:
        receipt_section = '''
<!-- ===== فیش پرداخت ===== -->
{% if order.receipt_image %}
<div class="bg-white rounded-lg shadow p-6 mt-6">
    <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
        <i class="fas fa-receipt text-emerald-600"></i>
        فیش پرداخت
    </h2>

    <div class="border-2 border-gray-200 rounded-xl overflow-hidden mb-4">
        <img src="{{ order.receipt_image }}" alt="فیش پرداخت" class="w-full max-h-96 object-contain bg-gray-50">
    </div>

    <div class="flex flex-wrap gap-3">
        <a href="{{ order.receipt_image }}" target="_blank"
           class="bg-blue-600 text-white px-5 py-3 rounded-lg hover:bg-blue-700 transition flex items-center gap-2">
            <i class="fas fa-eye"></i>
            مشاهده کامل
        </a>
        <a href="/admin/order/{{ order.id }}/receipt/download"
           class="bg-emerald-600 text-white px-5 py-3 rounded-lg hover:bg-emerald-700 transition flex items-center gap-2">
            <i class="fas fa-download"></i>
            دانلود فیش
        </a>
        <form action="/admin/order/{{ order.id }}/receipt/delete" method="POST"
              onsubmit="return confirm('آیا از حذف فیش مطمئن هستید؟')" class="inline">
            <button type="submit"
                    class="bg-red-500 text-white px-5 py-3 rounded-lg hover:bg-red-600 transition flex items-center gap-2">
                <i class="fas fa-trash"></i>
                حذف فیش
            </button>
        </form>
    </div>
</div>
{% else %}
<div class="bg-yellow-50 border-2 border-yellow-200 rounded-lg p-6 mt-6">
    <p class="text-yellow-800 flex items-center gap-2">
        <i class="fas fa-exclamation-triangle text-xl"></i>
        هنوز فیشی برای این سفارش آپلود نشده است.
    </p>
</div>
{% endif %}
'''

        # اضافه کردن قبل از {% endblock %}
        content = content.replace('{% endblock %}', receipt_section + '\n{% endblock %}')

        with open(admin_order_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ بخش فیش به admin/order_detail.html اضافه شد")

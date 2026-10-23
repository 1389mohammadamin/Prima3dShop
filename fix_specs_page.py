specs_path = 'app/interfaces/templates/admin/specifications.html'

html_content = '''{% extends "base.html" %}

{% block title %}مشخصات فنی {{ product.name }} - پریما استور{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
    <div class="flex justify-between items-center mb-8 border-b pb-4">
        <div>
            <h1 class="text-2xl font-bold text-gray-800">📊 مشخصات فنی: {{ product.name }}</h1>
            <p class="text-sm text-gray-500 mt-1">اینجا می‌توانید ویژگی‌های فنی محصول را تعریف کنید.</p>
        </div>
        <a href="/admin/products/edit/{{ product.id }}" class="text-gray-500 hover:text-emerald-600 transition text-sm flex items-center gap-1">
            <i class="fas fa-arrow-right"></i> بازگشت به ویرایش
        </a>
    </div>

    <!-- فرم افزودن مشخصات جدید -->
    <div class="bg-gray-50 p-6 rounded-xl border border-gray-200 mb-8">
        <h3 class="font-bold mb-4 text-gray-800">➕ افزودن مشخصات جدید</h3>
        <form action="/admin/products/{{ product.id }}/specifications/create" method="POST">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                    <label class="block text-sm font-semibold mb-2 text-gray-700">عنوان مشخصه *</label>
                    <input type="text" name="spec_key" placeholder="مثلاً: وزن، ابعاد، جنس" required 
                           class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 transition">
                </div>
                <div>
                    <label class="block text-sm font-semibold mb-2 text-gray-700">مقدار مشخصه *</label>
                    <input type="text" name="spec_value" placeholder="مثلاً: ۲۰۰ گرم، ۱۰×۵ سانتی‌متر" required 
                           class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 transition">
                </div>
                <div>
                    <label class="block text-sm font-semibold mb-2 text-gray-700">ترتیب نمایش (اختیاری)</label>
                    <input type="number" name="display_order" placeholder="مثلاً: 1" min="0" value="0"
                           class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 transition">
                </div>
            </div>
            <button type="submit" class="bg-emerald-600 text-white px-6 py-3 rounded-xl hover:bg-emerald-700 transition font-bold shadow-md">
                <i class="fas fa-plus ml-2"></i> افزودن مشخصه
            </button>
        </form>
    </div>

    <!-- لیست مشخصات موجود -->
    <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table class="w-full">
            <thead>
                <tr class="bg-gray-50 text-gray-600 text-sm">
                    <th class="px-6 py-4 text-right font-semibold">عنوان مشخصه</th>
                    <th class="px-6 py-4 text-right font-semibold">مقدار</th>
                    <th class="px-6 py-4 text-center font-semibold">ترتیب</th>
                    <th class="px-6 py-4 text-center font-semibold">عملیات</th>
                </tr>
            </thead>
            <tbody class="text-sm divide-y divide-gray-100">
                {% for spec in specs|sort(attribute='display_order') %}
                <tr class="hover:bg-gray-50 transition">
                    <td class="px-6 py-4 font-bold text-gray-800">{{ spec.spec_key }}</td>
                    <td class="px-6 py-4 text-gray-600">{{ spec.spec_value }}</td>
                    <td class="px-6 py-4 text-center text-gray-500">{{ spec.display_order }}</td>
                    <td class="px-6 py-4 text-center">
                        <form action="/admin/specifications/{{ spec.id }}/delete" method="POST" class="inline" onsubmit="return confirm('آیا از حذف این مشخصه مطمئن هستید؟')">
                            <button type="submit" class="bg-red-50 text-red-500 hover:bg-red-100 hover:text-red-700 p-2 rounded-lg transition" title="حذف">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </form>
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="4" class="px-6 py-12 text-center text-gray-400">
                        <i class="fas fa-table text-4xl mb-3 block"></i>
                        هنوز هیچ مشخصه فنی برای این محصول ثبت نشده است.
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
'''

with open(specs_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ صفحه مشخصات فنی (specifications.html) با موفقیت بازنویسی شد!")

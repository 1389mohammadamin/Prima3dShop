form_path = r'app\interfaces\templates\admin\product_form.html'
with open(form_path, 'r', encoding='utf-8') as f:
    content = f.read()

# چک کن لینک وجود داره یا نه
if 'admin_product_variants' not in content:
    links_html = '''
        {% if product %}
        <div class="mt-6 p-4 bg-emerald-50 rounded-xl border-2 border-emerald-200">
            <h3 class="font-bold text-lg mb-3 text-emerald-800">🎨 مدیریت تنوع و مشخصات</h3>
            <div class="flex flex-wrap gap-3">
                <a href="/admin/products/{{ product.id }}/variants" class="bg-emerald-600 text-white px-5 py-3 rounded-lg hover:bg-emerald-700 transition font-semibold inline-flex items-center gap-2">
                    <i class="fas fa-palette"></i> مدیریت رنگ‌ها
                </a>
                <a href="/admin/products/{{ product.id }}/specifications" class="bg-blue-600 text-white px-5 py-3 rounded-lg hover:bg-blue-700 transition font-semibold inline-flex items-center gap-2">
                    <i class="fas fa-table"></i> مدیریت مشخصات فنی
                </a>
            </div>
        </div>
        {% endif %}
'''

    # اضافه کردن قبل از دکمه‌های ذخیره
    if '<button type="submit"' in content:
        content = content.replace('<button type="submit"', links_html + '\n        <button type="submit"', 1)
    else:
        content = content.replace('</form>', links_html + '\n</form>')

    with open(form_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ لینک‌های مدیریت تنوع اضافه شدند')
else:
    print('✅ لینک‌ها قبلاً وجود دارند')

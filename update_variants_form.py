import re

# ۱. تغییر روت پایتون برای ارسال لیست رنگ‌ها به قالب
main_path = 'app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# پیدا کردن روت admin_product_variants و اضافه کردن colors به render_template
pattern = r"(@app\.route\('/admin/products/<int:product_id>/variants'\).*?def admin_product_variants\(product_id\):.*?return render_template\('admin/variants\.html', product=product, variants=variants\))"

if re.search(pattern, content, re.DOTALL):
    new_route = '''@app.route('/admin/products/<int:product_id>/variants')
@login_required
def admin_product_variants(product_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    product = Product.query.get_or_404(product_id)
    variants = ProductVariant.query.filter_by(product_id=product_id).all()
    # گرفتن لیست همه رنگ‌های سراسری
    global_colors = Color.query.order_by(Color.name).all()
    return render_template('admin/variants.html', product=product, variants=variants, colors=global_colors)'''

    content = re.sub(pattern, new_route, content, flags=re.DOTALL)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ روت variants آپدیت شد و لیست رنگ‌ها رو ارسال می‌کنه")

# ۲. تغییر قالب variants.html
variants_path = 'app/interfaces/templates/admin/variants.html'
with open(variants_path, 'r', encoding='utf-8') as f:
    v_content = f.read()

# پیدا کردن فرم افزودن رنگ
# ما فیلد name و color_code رو با یک منوی کشویی (select) جایگزین می‌کنیم
# و فیلد value رو هم برای اسم (مثلا قرمز) نگه می‌داریم

# نکته: چون در دیتابیس فیلد name برابر "رنگ" ذخیره میشه و value برابر اسم رنگ (قرمز)،
# ما در فرم جدید یک select می‌ذاریم که وقتی کاربر رنگ رو انتخاب می‌کنه،
# مقدار name (اسم رنگ) و color_code به صورت مخفی پر بشن.

form_pattern = r'<form action="/admin/products/\{\{ product\.id \}\}/variants/create" method="POST".*?</form>'

new_form = '''
<form action="/admin/products/{{ product.id }}/variants/create" method="POST" id="addVariantForm">
    <input type="hidden" name="name" value="رنگ">
    <input type="hidden" name="color_code" id="hiddenColorCode" value="">
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
        <div>
            <label class="block text-sm font-semibold mb-2 text-gray-700">انتخاب رنگ *</label>
            <select id="colorSelect" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500">
                <option value="" disabled selected>یک رنگ انتخاب کنید...</option>
                {% for color in colors %}
                <option value="{{ color.name }}" data-color-code="{{ color.color_code }}">{{ color.name }}</option>
                {% endfor %}
            </select>
        </div>
        
        <div>
            <label class="block text-sm font-semibold mb-2 text-gray-700">تغییر قیمت (تومان)</label>
            <input type="number" name="price_adjustment" placeholder="۰" step="1000" value="0" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500">
        </div>
        
        <div>
            <label class="block text-sm font-semibold mb-2 text-gray-700">موجودی *</label>
            <input type="number" name="quantity" placeholder="تعداد" min="0" value="1" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500">
        </div>

        <div>
            <label class="block text-sm font-semibold mb-2 text-gray-700">SKU *</label>
            <input type="text" name="sku" placeholder="کد محصول" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500">
        </div>
    </div>
    
    <button type="submit" class="bg-emerald-600 text-white px-6 py-3 rounded-lg hover:bg-emerald-700 transition font-semibold shadow-md">
        <i class="fas fa-plus ml-2"></i> افزودن رنگ به محصول
    </button>
</form>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        const colorSelect = document.getElementById('colorSelect');
        const hiddenColorCode = document.getElementById('hiddenColorCode');
        
        if (colorSelect) {
            colorSelect.addEventListener('change', function() {
                // وقتی رنگ انتخاب میشه، کد رنگش رو از data-color-code می‌خونیم
                const selectedOption = this.options[this.selectedIndex];
                if (selectedOption) {
                    hiddenColorCode.value = selectedOption.getAttribute('data-color-code');
                }
            });
        }
    });
</script>
'''

if re.search(form_pattern, v_content, re.DOTALL):
    v_content = re.sub(form_pattern, new_form, v_content, flags=re.DOTALL)
    with open(variants_path, 'w', encoding='utf-8') as f:
        f.write(v_content)
    print("✅ فرم افزودن رنگ به محصول با منوی کشویی آپدیت شد")
else:
    print("❌ فرم افزودن رنگ در variants.html پیدا نشد (شاید ساختار عوض شده).")

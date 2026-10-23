import re

form_path = 'app/interfaces/templates/admin/product_form.html'
with open(form_path, 'r', encoding='utf-8') as f:
    content = f.read()

# =============================================
# ۱. حذف کامل بخش گالری تصاویر (برای جلوگیری از تداخل)
# =============================================
# پیدا کردن از تگ <!-- گالری تصاویر --> تا قبل از بسته شدن div اصلی
# یا پیدا کردن باکس گالری با کلمه کلیدی "گالری تصاویر محصول"
gallery_pattern = r'<!-- باکس گالری تصاویر.*?</div>\s*(?=</div>|</body>|</html>)'
content = re.sub(gallery_pattern, '', content, flags=re.DOTALL)

# شاید کامنت متفاوت باشه، اینبار با کلمه کلیدی خودش حذف می‌کنیم
gallery_pattern_2 = r'<div class="mt-8 bg-white p-6 rounded-2xl border border-gray-200">\s*<h3[^>]*>.*?گالری تصاویر محصول.*?</div>\s*(?=</div>|</body>|</html>)'
content = re.sub(gallery_pattern_2, '', content, flags=re.DOTALL)

print("✅ بخش گالری تصاویر حذف شد")

# =============================================
# ۲. اضافه کردن باکس مدیریت رنگ و مشخصات (بعد از دکمه‌های فرم)
# =============================================
management_box = '''
    <!-- ===== لینک‌های مدیریت تنوع و مشخصات ===== -->
    {% if product %}
    <div class="mt-8 bg-emerald-50 rounded-2xl border-2 border-emerald-200 p-6">
        <h3 class="text-lg font-bold text-emerald-800 mb-4 flex items-center gap-2">
            <i class="fas fa-tools"></i> مدیریت تکمیلی محصول
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <a href="/admin/products/{{ product.id }}/variants" class="flex items-center justify-center gap-2 bg-white text-emerald-600 border border-emerald-200 px-6 py-4 rounded-xl hover:bg-emerald-100 transition font-bold shadow-sm">
                <i class="fas fa-palette text-xl"></i> مدیریت رنگ‌ها و تنوع
            </a>
            <a href="/admin/products/{{ product.id }}/specifications" class="flex items-center justify-center gap-2 bg-white text-emerald-600 border border-emerald-200 px-6 py-4 rounded-xl hover:bg-emerald-100 transition font-bold shadow-sm">
                <i class="fas fa-table text-xl"></i> مدیریت مشخصات فنی
            </a>
        </div>
    </div>
    {% endif %}
'''

# پیدا کردن محل آخرین فرم و اضافه کردن باکس بعد از اون
if 'مدیریت رنگ‌ها و تنوع' not in content:
    last_form_pos = content.rfind('</form>')
    if last_form_pos != -1:
        # اضافه کردن باکس بعد از تگ بسته شدن فرم
        content = content[:last_form_pos + 7] + '\n' + management_box + '\n' + content[last_form_pos + 7:]
        print("✅ باکس مدیریت رنگ و مشخصات اضافه شد")
    else:
        print("❌ تگ </form> پیدا نشد")

with open(form_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("🎉 تمام! حالا سرور رو ریستارت کن.")

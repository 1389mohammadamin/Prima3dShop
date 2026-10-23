form_path = 'app/interfaces/templates/admin/product_form.html'
with open(form_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ساخت باکس لینک‌های مدیریت
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

# اضافه کردن بعد از فرم اصلی (قبل از بسته شدن div اصلی)
# ما دنبال آخرین </form> می‌گردیم و باکس رو بعد از اون اضافه می‌کنیم
if 'مدیریت رنگ‌ها و تنوع' not in content:
    # پیدا کردن محل آخرین فرم
    last_form_pos = content.rfind('</form>')
    if last_form_pos != -1:
        content = content[:last_form_pos + 7] + '\n' + management_box + '\n' + content[last_form_pos + 7:]
        print("✅ باکس مدیریت رنگ و مشخصات به فرم اضافه شد")
    else:
        print("❌ تگ </form> پیدا نشد")
else:
    print("✅ باکس مدیریت از قبل وجود دارد")

with open(form_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("🎉 تمام! حالا سرور رو ریستارت کن.")

import re

form_path = 'app/interfaces/templates/admin/product_form.html'
with open(form_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ۱. حذف کدهای onkeyup قدیمی از تگ‌های input
content = re.sub(r'onkeyup="[^"]*"', '', content)

# ۲. تبدیل فیلدهای قیمت به type="text" (اگه type="number" باشن)
# این کار باعث میشه کاما قبول بشه
content = content.replace('<input type="number" name="price"', '<input type="text" name="price"')
content = content.replace('<input type="number" name="discount_price"', '<input type="text" name="discount_price"')

# ۳. اضافه کردن اسکریپت جاوااسکریپت جدید و قوی
# اول اسکریپت‌های قبلی مربوط به فرمت رو پاک می‌کنیم
content = re.sub(r'<script>\s*// جداکننده خودکار اعداد.*?</script>', '', content, flags=re.DOTALL)

script_code = '''
<script>
    document.addEventListener('DOMContentLoaded', function() {
        var priceInputs = document.querySelectorAll('input[name="price"], input[name="discount_price"]');
        
        priceInputs.forEach(function(input) {
            // مقداردهی اولیه: اگه مقدار داره، با کاما نمایش بده
            if (input.value) {
                let val = input.value.replace(/[^0-9]/g, '');
                if (val) {
                    input.value = val.replace(/\\B(?=(\\d{3})+(?!\\d))/g, ',');
                }
            }

            input.addEventListener('input', function(e) {
                // حذف هر چیزی غیر از عدد
                let value = this.value.replace(/[^0-9]/g, '');
                
                // اضافه کردن کاما
                if (value) {
                    this.value = value.replace(/\\B(?=(\\d{3})+(?!\\d))/g, ',');
                } else {
                    this.value = '';
                }
            });
        });
    });
</script>
'''

# اضافه کردن اسکریپت قبل از {% endblock %}
content = content.replace('{% endblock %}', script_code + '\n{% endblock %}')

# ذخیره فایل
with open(form_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ فرم محصول برای جداکننده اعداد اصلاح شد!")

form_path = 'app/interfaces/templates/admin/product_form.html'
with open(form_path, 'r', encoding='utf-8') as f:
    content = f.read()

# کد جاوااسکریپت برای فرمت‌دهی خودکار اعداد
script_code = '''
<script>
    // جداکننده خودکار اعداد (کاما)
    function formatNumberInput(input) {
        if (!input) return;
        
        // حذف هر کاراکتر غیر عددی
        let value = input.value.replace(/[^0-9]/g, '');
        
        // اگه خالی بود، چیزی نمایش نده
        if (!value) {
            input.value = '';
            return;
        }
        
        // اضافه کردن کاما به صورت ۳ رقم ۳ رقم
        input.value = value.replace(/\\B(?=(\\d{3})+(?!\\d))/g, ',');
    }

    // پیدا کردن فیلدهای قیمت و اعمال فرمت‌دهی
    document.addEventListener('DOMContentLoaded', function() {
        var priceInput = document.querySelector('input[name="price"]');
        var discountInput = document.querySelector('input[name="discount_price"]');

        if (priceInput) {
            priceInput.addEventListener('input', function() {
                formatNumberInput(this);
            });
        }

        if (discountInput) {
            discountInput.addEventListener('input', function() {
                formatNumberInput(this);
            });
        }
    });
</script>
'''

# اضافه کردن اسکریپت قبل از {% endblock %}
if 'formatNumberInput' not in content:
    content = content.replace('{% endblock %}', script_code + '\n{% endblock %}')
    with open(form_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ اسکریپت جداکننده اعداد به فرم اضافه شد")
else:
    print("✅ اسکریپت جداکننده اعداد از قبل وجود دارد")

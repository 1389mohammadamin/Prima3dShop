form_path = r'app\interfaces\templates\admin\product_form.html'
with open(form_path, 'r', encoding='utf-8') as f:
    content = f.read()

# اسکریپت فرمت قیمت
format_script = '''
<script>
    document.addEventListener('DOMContentLoaded', function() {
        var priceInput = document.querySelector('input[name="price"]');
        var discountInput = document.querySelector('input[name="discount_price"]');
        
        function formatNumber(input) {
            if (!input) return;
            
            input.addEventListener('input', function() {
                var value = this.value.replace(/[^0-9]/g, '');
                if (value.length > 0) {
                    var formatted = new Intl.NumberFormat('en-US').format(parseInt(value));
                    this.value = formatted;
                }
            });
            
            input.addEventListener('focus', function() {
                var value = this.value.replace(/[^0-9]/g, '');
                this.value = value;
            });
            
            input.addEventListener('blur', function() {
                var value = this.value.replace(/[^0-9]/g, '');
                if (value.length > 0) {
                    var formatted = new Intl.NumberFormat('en-US').format(parseInt(value));
                    this.value = formatted;
                }
            });
        }
        
        formatNumber(priceInput);
        formatNumber(discountInput);
    });
</script>
'''

# اضافه کردن قبل از {% endblock %}
content = content.replace('{% endblock %}', format_script + '\n{% endblock %}')

with open(form_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ فرمت خودکار قیمت اضافه شد')

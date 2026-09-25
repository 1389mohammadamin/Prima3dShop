form_path = r'app\interfaces\templates\admin\product_form.html'
with open(form_path, 'r', encoding='utf-8') as f:
    content = f.read()

# حذف اسکریپت قبلی
import re
content = re.sub(r'<script>\s*document\.addEventListener.*?</script>', '', content, flags=re.DOTALL)

# اسکریپت جدید با روش ساده
format_script = '''
<script>
    document.addEventListener('DOMContentLoaded', function() {
        function setupPriceFormat(input) {
            if (!input) return;
            
            input.addEventListener('input', function() {
                var cursorPos = this.selectionStart;
                var value = this.value.replace(/[^0-9]/g, '');
                var formatted = '';
                
                while (value.length > 3) {
                    formatted = ',' + value.slice(-3) + formatted;
                    value = value.slice(0, -3);
                }
                formatted = value + formatted;
                
                this.value = formatted;
                
                var newCursorPos = cursorPos + (formatted.length - this.value.length);
                this.setSelectionRange(newCursorPos, newCursorPos);
            });
        }
        
        setupPriceFormat(document.querySelector('input[name="price"]'));
        setupPriceFormat(document.querySelector('input[name="discount_price"]'));
    });
</script>
'''

# اضافه کردن قبل از {% endblock %}
content = content.replace('{% endblock %}', format_script + '\n{% endblock %}')

with open(form_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ فرمت قیمت فیکس شد')

form_path = r'app\interfaces\templates\admin\product_form.html'
with open(form_path, 'r', encoding='utf-8') as f:
    content = f.read()

# حذف همه اسکریپت‌های قبلی
import re
content = re.sub(r'<script>.*?</script>', '', content, flags=re.DOTALL)

# حذف بک‌تیک‌های اضافی
content = content.replace('`n', '')

# اسکریپت خیلی ساده
simple_script = '''
<script>
function formatPrice(el) {
    el.addEventListener('keyup', function() {
        var val = this.value.replace(/,/g, '');
        if (val.length > 3) {
            var parts = [];
            while (val.length > 3) {
                parts.unshift(val.slice(-3));
                val = val.slice(0, val.length - 3);
            }
            parts.unshift(val);
            this.value = parts.join(',');
        } else {
            this.value = val;
        }
    });
}
formatPrice(document.querySelector('input[name="price"]'));
formatPrice(document.querySelector('input[name="discount_price"]'));
</script>
'''

# اضافه کردن قبل از {% endblock %}
content = content.replace('{% endblock %}', simple_script + '\n{% endblock %}')

with open(form_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ اسکریپت ساده اضافه شد')

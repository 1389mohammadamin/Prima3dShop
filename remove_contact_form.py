import re

contact_path = 'app/interfaces/templates/contact.html'
with open(contact_path, 'r', encoding='utf-8') as f:
    content = f.read()

# حذف کل ستون فرم ارسال پیام
# الگو: از <!-- ستون دوم: فرم تماس --> تا قبل از </div> که کل گرید رو میبنده
form_pattern = r'<!-- ستون دوم: فرم تماس -->.*?(?=</div>\s*</div>\s*<script>)'

content = re.sub(form_pattern, '', content, flags=re.DOTALL)

# حالا چون فرم حذف شده باید ستون اطلاعات تماس رو وسطچین کنیم
# کلاس grid-cols-2 رو به max-w-2xl و mx-auto تغییر میدیم تا اطلاعات تماس وسط صفحه قرار بگیره
content = content.replace(
    '<div class="grid grid-cols-1 md:grid-cols-2 gap-8">',
    '<div class="max-w-2xl mx-auto">'
)

with open(contact_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ فرم ارسال پیام حذف شد و اطلاعات تماس وسطچین شدند.")

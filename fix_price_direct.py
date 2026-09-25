form_path = r'app\interfaces\templates\admin\product_form.html'
with open(form_path, 'r', encoding='utf-8') as f:
    content = f.read()

# پیدا کردن input قیمت و تغییر مستقیم
old_price = '<input type="number" name="price"'
new_price = '<input type="text" name="price" inputmode="numeric" onkeyup="this.value = this.value.replace(/[^0-9]/g, \'\').replace(/\\B(?=(\\d{3})+(?!\\d))/g, \',\')"'

content = content.replace(old_price, new_price)

old_discount = '<input type="number" name="discount_price"'
new_discount = '<input type="text" name="discount_price" inputmode="numeric" onkeyup="this.value = this.value.replace(/[^0-9]/g, \'\').replace(/\\B(?=(\\d{3})+(?!\\d))/g, \',\')"'

content = content.replace(old_discount, new_discount)

with open(form_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ فیلد قیمت با فرمت مستقیم عوض شد')

variants_path = r'app\interfaces\templates\admin\variants.html'
with open(variants_path, 'r', encoding='utf-8') as f:
    content = f.read()

# حذف خطوط csrf_token
content = content.replace('            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">\n', '')
content = content.replace('                            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">\n', '')
content = content.replace('<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">', '')

with open(variants_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ csrf_token از variants.html حذف شد')

base_path = 'app/interfaces/templates/base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

# جایگزینی لینک CSS با اسکریپت JS لوکال
# ما Tailwind رو به صورت JS دانلود کردیم، پس باید به صورت script لود بشه
content = content.replace(
    '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/tailwind.css\') }}">',
    '<script src="{{ url_for(\'static\', filename=\'js/tailwind.js\') }}"></script>'
)

# اگه هنوز لینک قدیمی هست، مستقیم عوضش کن
content = content.replace(
    '<script src="https://cdn.tailwindcss.com"></script>',
    '<script src="{{ url_for(\'static\', filename=\'js/tailwind.js\') }}"></script>'
)

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ base.html برای Tailwind لوکال آپدیت شد')

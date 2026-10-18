base_path = 'app/interfaces/templates/base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

# تغییر پسوند به jpg
content = content.replace("images/logo.png", "images/logo.jpg")

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ پسوند لوگو به jpg تغییر کرد")

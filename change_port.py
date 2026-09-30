run_path = r'run.py'
with open(run_path, 'r', encoding='utf-8') as f:
    content = f.read()

# تغییر پورت به 80
import re
content = re.sub(r"port\s*=\s*int\(os\.environ\.get\('PORT',\s*\d+\)\)", 
                 "port = int(os.environ.get('PORT', 80))", content)
content = re.sub(r"app\.run\([^)]*port\s*=\s*\d+[^)]*\)", 
                 "app.run(host='0.0.0.0', port=80, debug=False)", content)

with open(run_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ پورت به 80 تغییر کرد')
print(content)

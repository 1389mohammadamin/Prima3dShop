# check_routes.py
from app.main import create_app

app = create_app()

print("\n📋 لیست همه مسیرهای ثبت شده:")
print("="*60)
for rule in app.url_map.iter_rules():
    print(f"  {rule.endpoint}: {rule}")
print("="*60)
print(f"\n✅ تعداد کل مسیرها: {len(app.url_map._rules)}")
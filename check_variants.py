main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=== بررسی وضعیت فعلی ===")
print(f"ProductVariant: {'✅' if 'class ProductVariant' in content else '❌'}")
print(f"admin_product_variants: {'✅' if 'def admin_product_variants' in content else '❌'}")
print(f"admin_variant_create: {'✅' if 'def admin_variant_create' in content else '❌'}")
print(f"ProductSpecification: {'✅' if 'class ProductSpecification' in content else '❌'}")

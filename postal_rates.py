# postal_rates.py - محاسبه هزینه پست پیشتاز
from decimal import Decimal

# استان‌های همجوار تهران
NEIGHBOR_PROVINCES = ['البرز', 'قم', 'مرکزی', 'سمنان', 'مازندران', 'قزوین']

# تعرفه‌های پایه ۱۴۰۴ (ریال) - برای ۱۴۰۵ در 1.6 ضرب کن
RATES_1404 = {
    'local': Decimal('218000'),      # درون استانی
    'neighbor': Decimal('281200'),   # همجوار
    'far': Decimal('370000'),        # غیرهمجوار
}

# ضریب افزایش ۱۴۰۵
RATE_MULTIPLIER = Decimal('1.6')

def get_zone(province):
    """تشخیص رده مسافتی بر اساس استان مقصد"""
    if province == 'تهران':
        return 'local'
    elif province in NEIGHBOR_PROVINCES:
        return 'neighbor'
    else:
        return 'far'

def calculate_shipping(destination_province, weight_kg=1):
    """محاسبه هزینه پست بر اساس استان مقصد و وزن"""
    zone = get_zone(destination_province)
    base_rate = RATES_1404[zone] * RATE_MULTIPLIER
    
    # مازاد بر ۱ کیلوگرم
    if weight_kg > 1:
        extra_kg = weight_kg - 1
        extra_rate = Decimal('80000') * RATE_MULTIPLIER * Decimal(str(extra_kg))
        base_rate += extra_rate
    
    return int(base_rate)

# تست
print("تهران:", calculate_shipping('تهران'))
print("البرز (همجوار):", calculate_shipping('البرز'))
print("اصفهان (غیرهمجوار):", calculate_shipping('اصفهان'))

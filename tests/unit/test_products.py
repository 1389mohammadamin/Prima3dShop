import pytest
from decimal import Decimal
from app.domain.entities.product import ProductEntity
from app.application.use_cases.product_use_cases import ProductUseCases

class MockProductRepository:
    """ریپازیتوری ساختگی برای تست"""
    def __init__(self):
        self.products = {}
        self.next_id = 1
    
    def save(self, product):
        if not product.id:
            product.id = self.next_id
            self.next_id += 1
        self.products[product.id] = product
        return product
    
    def find_by_id(self, product_id):
        return self.products.get(product_id)
    
    def find_by_category(self, category_id):
        return [p for p in self.products.values() if p.category_id == category_id]
    
    def update(self, product):
        self.products[product.id] = product
        return product
    
    def delete(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False

def test_create_product():
    """تست ایجاد محصول"""
    repo = MockProductRepository()
    use_cases = ProductUseCases(repo)
    
    product_data = {
        'name': 'Test Product',
        'description': 'Test Description',
        'price': 100.00,
        'quantity': 10,
        'category_id': 1,
        'user_id': 1
    }
    
    product = use_cases.create_product(product_data)
    
    assert product.id is not None
    assert product.name == 'Test Product'
    assert product.price == Decimal('100.00')
    assert product.quantity == 10

def test_get_product_by_id():
    """تست دریافت محصول با ID"""
    repo = MockProductRepository()
    use_cases = ProductUseCases(repo)
    
    # ایجاد محصول تست
    product_data = {
        'name': 'Test Product',
        'price': 100.00,
        'quantity': 10,
        'category_id': 1,
        'user_id': 1
    }
    created = use_cases.create_product(product_data)
    
    # دریافت محصول
    found = use_cases.get_product_by_id(created.id)
    
    assert found is not None
    assert found.id == created.id
    assert found.name == 'Test Product'

def test_update_product():
    """تست به‌روزرسانی محصول"""
    repo = MockProductRepository()
    use_cases = ProductUseCases(repo)
    
    # ایجاد محصول
    product_data = {
        'name': 'Test Product',
        'price': 100.00,
        'quantity': 10,
        'category_id': 1,
        'user_id': 1
    }
    product = use_cases.create_product(product_data)
    
    # به‌روزرسانی
    update_data = {
        'name': 'Updated Product',
        'price': 150.00,
        'quantity': 20
    }
    updated = use_cases.update_product(product.id, update_data)
    
    assert updated.name == 'Updated Product'
    assert updated.price == Decimal('150.00')
    assert updated.quantity == 20
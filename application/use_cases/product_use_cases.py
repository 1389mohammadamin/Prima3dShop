from typing import List, Optional
from decimal import Decimal
from app.domain.entities.product import ProductEntity
from app.application.interfaces.repositories import ProductRepository

class ProductUseCases:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def create_product(self, product_data: dict) -> ProductEntity:
        """ایجاد محصول جدید"""
        # اعتبارسنجی
        if product_data.get('price', 0) <= 0:
            raise ValueError("Price must be greater than zero")
        
        if product_data.get('quantity', 0) < 0:
            raise ValueError("Quantity cannot be negative")
        
        # ایجاد product entity
        product = ProductEntity(
            name=product_data['name'],
            description=product_data.get('description', ''),
            price=Decimal(str(product_data['price'])),
            quantity=product_data.get('quantity', 0),
            category_id=product_data['category_id'],
            user_id=product_data['user_id']
        )
        
        # ذخیره در دیتابیس
        return self.product_repository.save(product)
    
    def get_product_by_id(self, product_id: int) -> Optional[ProductEntity]:
        """دریافت محصول با ID"""
        return self.product_repository.find_by_id(product_id)
    
    def get_products_by_category(self, category_id: int) -> List[ProductEntity]:
        """دریافت محصولات یک دسته"""
        return self.product_repository.find_by_category(category_id)
    
    def update_product(self, product_id: int, product_data: dict) -> ProductEntity:
        """به‌روزرسانی محصول"""
        product = self.product_repository.find_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        
        # به‌روزرسانی فیلدها
        if 'name' in product_data:
            product.name = product_data['name']
        if 'price' in product_data:
            product.price = Decimal(str(product_data['price']))
        if 'quantity' in product_data:
            product.quantity = product_data['quantity']
        
        return self.product_repository.update(product)
    
    def delete_product(self, product_id: int) -> bool:
        """حذف محصول"""
        return self.product_repository.delete(product_id)
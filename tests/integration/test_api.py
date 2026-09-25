import pytest
from flask import json

def test_get_products(client):
    """تست دریافت لیست محصولات"""
    response = client.get('/api/products')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_create_product_api(client, auth_token):
    """تست ایجاد محصول از طریق API"""
    headers = {'Authorization': f'Bearer {auth_token}'}
    product_data = {
        'name': 'API Test Product',
        'description': 'Test from API',
        'price': 99.99,
        'quantity': 5,
        'category_id': 1
    }
    
    response = client.post('/api/products', 
                          json=product_data,
                          headers=headers)
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'API Test Product'
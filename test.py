import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['database'] == 'connected'

def test_get_products(client):
    """Test products endpoint"""
    response = client.get('/products')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0
    assert 'name' in data[0]
    assert 'price' in data[0]

def test_add_to_cart(client):
    """Test adding item to cart"""
    cart_data = {
        'product_id': 1,
        'quantity': 2,
        'user_id': 'test_user'
    }
    
    response = client.post('/cart', 
                         data=json.dumps(cart_data),
                         content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Product added to cart successfully'

def test_get_cart(client):
    """Test getting cart items"""
    response = client.get('/cart?user_id=test_user')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items' in data
    assert 'total_price' in data

def test_categories(client):
    """Test categories endpoint"""
    response = client.get('/categories')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
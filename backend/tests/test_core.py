import pytest
from django.contrib.auth.models import User
from base.models import Product, Order, OrderItem
from base.serializers import ProductSerializer, OrderSerializer

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', email='test@test.com', password='password123')

@pytest.fixture
def product(user):
    return Product.objects.create(
        user=user,
        name='Test Product',
        price=100.00,
        countInStock=10
    )

@pytest.fixture
def order(user):
    return Order.objects.create(
        user=user,
        taxPrice=10.00,
        shippingPrice=5.00,
        totalPrice=115.00
    )

@pytest.mark.django_db
def test_create_product(product):
    assert product.name == 'Test Product'
    assert product.price == 100.00
    assert product.countInStock == 10

@pytest.mark.django_db
def test_product_str(product):
    assert str(product) == 'Test Product'

@pytest.mark.django_db
def test_product_serializer(product):
    serializer = ProductSerializer(product)
    assert serializer.data['name'] == 'Test Product'
    assert float(serializer.data['price']) == 100.00

@pytest.mark.django_db
def test_create_order_total_price(order, product):
    # Simulate total price calculation
    item = OrderItem.objects.create(
        order=order,
        product=product,
        name=product.name,
        qty=2,
        price=product.price
    )
    items_price = item.qty * item.price
    calculated_total = items_price + order.taxPrice + order.shippingPrice
    
    assert calculated_total == 215.00
    assert order.totalPrice == 115.00  # Initial price from fixture

@pytest.mark.django_db
def test_order_str(order):
    assert str(order) == str(order.createdAt)

@pytest.mark.django_db
def test_order_serializer(order):
    serializer = OrderSerializer(order)
    assert float(serializer.data['taxPrice']) == 10.00
    assert float(serializer.data['shippingPrice']) == 5.00

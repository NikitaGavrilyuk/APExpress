import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from base.models import Product, Order, OrderItem, ShippingAddress

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', email='test@test.com', password='password123')

@pytest.fixture
def other_user():
    return User.objects.create_user(username='otheruser', email='other@test.com', password='password123')

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
        paymentMethod="Після отримання",
        taxPrice=0,
        shippingPrice=0,
        totalPrice=100.00
    )

@pytest.mark.django_db
def test_get_delivery_branches(client):
    url = reverse('delivery-branches')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 8 # 8 default branches

@pytest.mark.django_db
def test_get_delivery_branches_with_city_filter(client):
    url = reverse('delivery-branches')
    response = client.get(url, {'city': 'Київ'})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    for branch in response.data:
        assert branch['city'] == 'Київ'

@pytest.mark.django_db
def test_add_order_items_unauthenticated(client):
    url = reverse('orders-add')
    response = client.post(url, {})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_add_order_items_empty_cart(client, user):
    client.force_authenticate(user=user)
    url = reverse('orders-add')
    response = client.post(url, {'orderItems': []})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['detail'] == 'Кошик порожній. Додайте товари для оформлення замовлення.'

@pytest.mark.django_db
def test_add_order_items_success(client, user, product):
    client.force_authenticate(user=user)
    url = reverse('orders-add')
    data = {
        'orderItems': [
            {'product': product._id, 'qty': 2, 'price': 100.00}
        ],
        'shippingAddress': {
            'address': 'Test Address',
            'city': 'Test City',
            'postalCode': '12345',
            'country': 'Ukraine'
        },
        'paymentMethod': 'Після отримання',
        'totalPrice': 200.00
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'Замовлення створено успішно!' in response.data['message']

    # WMS Mock verification
    product.refresh_from_db()
    assert product.countInStock == 8 # 10 - 2

@pytest.mark.django_db
def test_get_order_by_id_unauthenticated(client, order):
    url = reverse('user-order', kwargs={'pk': order._id})
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_get_order_by_id_success(client, user, order):
    client.force_authenticate(user=user)
    url = reverse('user-order', kwargs={'pk': order._id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['_id'] == order._id

@pytest.mark.django_db
def test_get_order_by_id_not_found(client, user):
    client.force_authenticate(user=user)
    url = reverse('user-order', kwargs={'pk': 9999})
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_get_order_by_id_forbidden(client, other_user, order):
    client.force_authenticate(user=other_user)
    url = reverse('user-order', kwargs={'pk': order._id})
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_mock_pay_order_unauthenticated(client, order):
    url = reverse('pay-order', kwargs={'pk': order._id})
    response = client.put(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_mock_pay_order_success(client, user, order):
    client.force_authenticate(user=user)
    url = reverse('pay-order', kwargs={'pk': order._id})
    response = client.put(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['isPaid'] == True

    order.refresh_from_db()
    assert order.isPaid == True
    assert order.paidAt is not None

@pytest.mark.django_db
def test_mock_pay_order_not_found(client, user):
    client.force_authenticate(user=user)
    url = reverse('pay-order', kwargs={'pk': 9999})
    response = client.put(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_get_my_orders_unauthenticated(client):
    url = reverse('my-orders')
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_get_my_orders_success(client, user, order):
    client.force_authenticate(user=user)
    url = reverse('my-orders')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['_id'] == order._id

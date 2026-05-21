import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from base.models import Product, Review

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', email='test@test.com', password='password123')

@pytest.fixture
def product(user):
    return Product.objects.create(
        user=user,
        name='Test Product',
        price=100.00,
        countInStock=10,
        rating=4.5,
        numReviews=1
    )

@pytest.fixture
def product2(user):
    return Product.objects.create(
        user=user,
        name='Another Product',
        price=50.00,
        countInStock=5,
        rating=3.0,
        numReviews=0
    )

@pytest.mark.django_db
def test_get_products(client, product, product2):
    url = reverse('products')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['products']) == 2
    assert response.data['page'] == 1

@pytest.mark.django_db
def test_get_products_with_keyword(client, product, product2):
    url = reverse('products')
    response = client.get(url, {'keyword': 'Another'})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['products']) == 1
    assert response.data['products'][0]['name'] == 'Another Product'

@pytest.mark.django_db
def test_get_products_not_found(client, product):
    url = reverse('products')
    response = client.get(url, {'keyword': 'NonExistent'})
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_get_top_products(client, product, product2):
    url = reverse('top-products')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Product'

@pytest.mark.django_db
def test_get_product_by_id(client, product):
    url = reverse('product', kwargs={'pk': product._id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Test Product'

@pytest.mark.django_db
def test_create_product_review_unauthenticated(client, product):
    url = reverse('create-review', kwargs={'pk': product._id})
    response = client.post(url, {'rating': 5, 'comment': 'Great!'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_create_product_review_success(client, user, product):
    client.force_authenticate(user=user)
    url = reverse('create-review', kwargs={'pk': product._id})
    response = client.post(url, {'rating': 5, 'comment': 'Great!'}, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data == 'Review Added'
    
    product.refresh_from_db()
    assert product.numReviews == 1
    assert Review.objects.filter(product=product, user=user).exists()

@pytest.mark.django_db
def test_create_product_review_already_exists(client, user, product):
    Review.objects.create(user=user, product=product, name=user.first_name, rating=4, comment='Good')
    client.force_authenticate(user=user)
    url = reverse('create-review', kwargs={'pk': product._id})
    response = client.post(url, {'rating': 5, 'comment': 'Great!'}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['detail'] == 'Product Already Reviewed'

@pytest.mark.django_db
def test_create_product_review_no_rating(client, user, product):
    client.force_authenticate(user=user)
    url = reverse('create-review', kwargs={'pk': product._id})
    response = client.post(url, {'rating': 0, 'comment': 'Great!'}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['detail'] == 'Please Select A Rating'

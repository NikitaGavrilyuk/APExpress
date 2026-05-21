import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from base.models import Product
from ai_assistant.rag_service import generate_rag_response

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
        name='Масляний фільтр BMW',
        description='Оригінальний масляний фільтр для BMW',
        price=500.00,
        countInStock=10,
        category='Engine'
    )

@pytest.mark.django_db
@patch('ai_assistant.rag_service.client.chat.completions.create')
def test_generate_rag_response_success(mock_create):
    # Mocking the OpenAI API response
    mock_message = MagicMock()
    mock_message.content = "Це найкращий масляний фільтр для вашого BMW."
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_create.return_value = mock_response

    response = generate_rag_response("Який фільтр обрати?", "Engine", "[]")
    
    assert response == "Це найкращий масляний фільтр для вашого BMW."
    mock_create.assert_called_once()

@pytest.mark.django_db
@patch('ai_assistant.rag_service.client.chat.completions.create')
def test_generate_rag_response_rate_limit(mock_create):
    mock_create.side_effect = Exception("429 Rate limit exceeded")
    
    response = generate_rag_response("Який фільтр обрати?", "Engine", "[]")
    
    assert "перевищено ліміт запитів" in response

@pytest.mark.django_db
@patch('ai_assistant.rag_service.client.chat.completions.create')
def test_generate_rag_response_generic_error(mock_create):
    mock_create.side_effect = Exception("API Server Error")
    
    response = generate_rag_response("Який фільтр обрати?", "Engine", "[]")
    
    assert "Помилка при генерації відповіді" in response

@pytest.mark.django_db
@patch('ai_assistant.views.generate_rag_response')
@patch('ai_assistant.views.classify_query')
def test_chat_view_success(mock_classify, mock_generate, client, product):
    mock_classify.return_value = 'Engine'
    mock_generate.return_value = "Рекомендую цей масляний фільтр."
    
    url = reverse('chat')
    response = client.post(url, {'message': 'Масляний фільтр BMW'})
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['response'] == "Рекомендую цей масляний фільтр."
    assert response.data['category'] == 'Engine'
    assert len(response.data['products']) == 1
    assert response.data['products'][0]['name'] == 'Масляний фільтр BMW'

@pytest.mark.django_db
def test_chat_view_empty_message(client):
    url = reverse('chat')
    response = client.post(url, {'message': '   '})
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'Повідомлення не може бути порожнім.'

@pytest.mark.django_db
@patch('ai_assistant.views.generate_rag_response')
@patch('ai_assistant.views.classify_query')
def test_chat_view_general_category(mock_classify, mock_generate, client, product):
    mock_classify.return_value = 'General'
    mock_generate.return_value = "Загальна відповідь."
    
    url = reverse('chat')
    response = client.post(url, {'message': 'Привіт'})
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['category'] == 'General'
    assert len(response.data['products']) == 1
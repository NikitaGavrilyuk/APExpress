"""
Chat API endpoint for the Intelligent RAG Assistant.
Receives a user message, classifies it, retrieves matching products,
and generates an AI-powered recommendation.
"""

import json
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from base.models import Product
from .serializers import ChatProductSerializer
from .classifier import classify_query
from .rag_service import generate_rag_response


@api_view(["POST"])
@permission_classes([AllowAny])
def chat_view(request):
    """
    POST /api/chat/
    Body: {"message": "Потрібен масляний фільтр для BMW"}
    Response: {"response": "AI text...", "category": "Engine", "products": [...]}
    """
    message = request.data.get("message", "").strip()

    if not message:
        return Response(
            {"error": "Повідомлення не може бути порожнім."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 1. Classify the query
    category = classify_query(message)

    # 2. Retrieve matching products (Retrieval step)
    if category != "General":
        category_products = Product.objects.filter(category__iexact=category)

        # Secondary filter: narrow down by query keywords in name/description
        query_words = [w for w in message.lower().split() if len(w) > 2]
        q_filter = Q()
        for word in query_words:
            q_filter |= Q(name__icontains=word) | Q(description__icontains=word)

        specific_products = category_products.filter(q_filter)
        products = specific_products if specific_products.exists() else category_products
    else:
        products = Product.objects.all()[:10]

    serializer = ChatProductSerializer(products, many=True)

    # 3. Build context string for the LLM
    context_products = json.dumps(serializer.data, ensure_ascii=False)

    # 4. Generate AI response (Generation step)
    ai_response = generate_rag_response(message, category, context_products)

    return Response(
        {
            "response": ai_response,
            "category": category,
            "products": serializer.data,
        },
        status=status.HTTP_200_OK,
    )
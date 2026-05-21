"""
Order management views with mock external system integrations:
- Order creation with WMS stock reduction
- Mock payment processing
- Mock delivery branches (Nova Poshta)
"""

from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import OrderSerializer


# ─── Static mock data: Nova Poshta branches ───────────────────────
NOVA_POSHTA_BRANCHES = [
    {"id": 1, "city": "Київ",       "branch": "Відділення №1: вул. Хрещатик, 22"},
    {"id": 2, "city": "Київ",       "branch": "Відділення №15: пр. Перемоги, 67"},
    {"id": 3, "city": "Львів",      "branch": "Відділення №3: вул. Городоцька, 191"},
    {"id": 4, "city": "Одеса",      "branch": "Відділення №7: вул. Рішельєвська, 33"},
    {"id": 5, "city": "Харків",     "branch": "Відділення №12: вул. Пушкінська, 45"},
    {"id": 6, "city": "Дніпро",     "branch": "Відділення №5: пр. Яворницького, 88"},
    {"id": 7, "city": "Запоріжжя",  "branch": "Відділення №2: пр. Соборний, 120"},
    {"id": 8, "city": "Вінниця",    "branch": "Відділення №4: вул. Соборна, 55"},
]


@api_view(["GET"])
@permission_classes([AllowAny])
def get_delivery_branches(request):
    """
    GET /api/orders/delivery-branches/
    Mock Nova Poshta API — returns static list of branches.
    """
    city = request.query_params.get("city", "").strip().lower()
    if city:
        branches = [b for b in NOVA_POSHTA_BRANCHES if city in b["city"].lower()]
    else:
        branches = NOVA_POSHTA_BRANCHES
    return Response(branches)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_order_items(request):
    """
    POST /api/orders/add/
    Creates an Order + OrderItems + ShippingAddress.
    WMS Mock: reduces Product.countInStock for each item.
    """
    user = request.user
    data = request.data

    order_items = data.get("orderItems", [])
    if not order_items or len(order_items) == 0:
        return Response(
            {"detail": "Кошик порожній. Додайте товари для оформлення замовлення."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 1. Create order
    order = Order.objects.create(
        user=user,
        paymentMethod=data.get("paymentMethod", "Після отримання"),
        taxPrice=0,
        shippingPrice=0,
        totalPrice=data.get("totalPrice", 0),
    )

    # 2. Create shipping address
    shipping = data.get("shippingAddress", {})
    ShippingAddress.objects.create(
        order=order,
        address=shipping.get("address", ""),
        city=shipping.get("city", ""),
        postalCode=shipping.get("postalCode", ""),
        country=shipping.get("country", "Україна"),
    )

    # 3. Create order items + WMS stock reduction
    for item in order_items:
        product = Product.objects.get(_id=item["product"])

        OrderItem.objects.create(
            product=product,
            order=order,
            name=product.name,
            qty=item["qty"],
            price=item["price"],
            image=product.image.url if product.image else "",
        )

        # ── WMS MOCK: Reduce stock ──
        product.countInStock = max(0, product.countInStock - item["qty"])
        product.save()

    return Response({"_id": order._id, "message": "Замовлення створено успішно!"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, pk):
    """
    GET /api/orders/<id>/
    Returns order details.
    """
    try:
        order = Order.objects.get(_id=pk)
    except Order.DoesNotExist:
        return Response(
            {"detail": "Замовлення не знайдено."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if not request.user.is_staff and order.user != request.user:
        return Response(
            {"detail": "Немає доступу до цього замовлення."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def mock_pay_order(request, pk):
    """
    PUT /api/orders/<id>/pay/
    MOCK PAYMENT: Simulates successful payment.
    Sets isPaid=True, paidAt=now().
    """
    try:
        order = Order.objects.get(_id=pk)
    except Order.DoesNotExist:
        return Response(
            {"detail": "Замовлення не знайдено."},
            status=status.HTTP_404_NOT_FOUND,
        )

    order.isPaid = True
    order.paidAt = timezone.now()
    order.save()

    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    """
    GET /api/orders/myorders/
    Returns current user's orders.
    """
    orders = Order.objects.filter(user=request.user).order_by("-createdAt")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

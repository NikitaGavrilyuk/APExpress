from django.urls import path
from base.views import order_views as views

urlpatterns = [
    path('add/', views.add_order_items, name='orders-add'),
    path('myorders/', views.get_my_orders, name='my-orders'),
    path('delivery-branches/', views.get_delivery_branches, name='delivery-branches'),
    path('<str:pk>/', views.get_order_by_id, name='user-order'),
    path('<str:pk>/pay/', views.mock_pay_order, name='pay-order'),
]

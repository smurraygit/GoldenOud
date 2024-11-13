# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/<str:order_number>/', views.payments, name='payments'),
    path('order-complete/', views.order_complete, name='stripe_return'),  # Ensure this name matches
]

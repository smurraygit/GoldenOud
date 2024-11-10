from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_guest/', views.register_guest, name='register_guest'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/',
         views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('order_detail/<int:order_id>/',views.order_detail, name='order_detail'),
     path('admin_orders_list/', views.admin_order_list, name='admin_order_list'),
      path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
       path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
        path('update-order-status/<str:order_number>/', views.update_order_status, name='update_order_status'),
        

]

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', views.UserLoginView.as_view(), name = 'login'),
    path('edit_profile/', views.edit_profile, name = 'edit_profile'),
    path('change_password/', views.pass_change, name = 'change_password'),
    path('logout/', views.user_logout, name = 'logout'),
    path('profile/', views.OrderHistoryView.as_view(), name='order_history'),
    path('order/buy/<int:id>', views.buy_car, name='order_buy'),
]

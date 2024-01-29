from django.urls import path
from . import views

urlpatterns = [
    path('details/<int:id>', views.DetailCarView.as_view(), name = 'details_car'),
]

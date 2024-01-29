from django.db import models
from django.contrib.auth.models import User
from cars.models import Car

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.car.name
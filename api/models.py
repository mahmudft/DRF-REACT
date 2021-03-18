from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import empty

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True, unique=True, auto_created=True, )
    title = models.CharField(max_length=200)
    photo = models.ImageField()
    count = models.IntegerField(default=0)
    description = models.TextField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    track_id = models.AutoField(primary_key=True, unique=True, auto_created=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    payed = models.BooleanField(default=False)
    number = models.IntegerField()

    def __str__(self) -> str:
        return self.product.title

   
    def get_total(self) -> float:
        return self.number * self.product.price







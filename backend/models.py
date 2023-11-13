from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    name    = models.TextField(max_length=255)
    type    = models.TextField(max_length=255)

class TrashComponent(models.Model):
	name        = models.TextField(max_length=255)
	recyclable  = models.TextField(max_length=255)
	mass        = models.SmallIntegerField()

class Product(models.Model):
	name    = models.TextField(max_length=255)
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	type    = models.TextField(max_length=255)      
            # для того, чтобы можно было посоветовать более 
            # перерабатываемые альтернативы, типа если это молоко,
            # то ищем другие продукты вида "молоко", у которых больше
            # перерабатываемость
	trash   = models.ManyToManyField(TrashComponent)

class Receipt(models.Model):
    products    = models.ManyToManyField(Product)
    time        = models.DateTimeField()
    place       = models.TextField(max_length=255)
    user        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # user        = models.ForeignKey(User, on_delete=models.SET_NULL)

from django.contrib import admin

# Register your models here.
from backend import models

admin.site.register(models.Receipt)
admin.site.register(models.Product)
admin.site.register(models.Company)
admin.site.register(models.TrashComponent)

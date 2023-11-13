from django.contrib.auth.models import User
from rest_framework import serializers

from backend import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=255)
    access = serializers.CharField(max_length=255)
class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=255)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ['name', 'type', 'pk']
class CompanyPutSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    class Meta:
        model = models.Company
        fields = ['pk', 'name', 'type']


class TrashComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TrashComponent
        fields = ['name', 'recyclable', 'mass', 'pk']
class TrashComponentPutSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    class Meta:
        model = models.TrashComponent
        fields = ['pk', 'name', 'recyclable', 'mass']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['name', 'company', 'type', 'trash', 'pk']
class ProductPutSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    class Meta:
        model = models.Product
        fields = ['pk', 'name', 'company', 'type', 'trash']


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Receipt
        fields = ['products', 'time', 'place', 'pk']
class ReceiptGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Receipt
        fields = ['products', 'time', 'place', 'pk', 'user']
class ReceiptPutSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    class Meta:
        model = models.Receipt
        fields = ['pk', 'products', 'time', 'place']

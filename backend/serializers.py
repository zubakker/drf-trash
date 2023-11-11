from rest_framework import serializers

from backend import models


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
class ReceiptPutSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    class Meta:
        model = models.Receipt
        fields = ['pk', 'products', 'time', 'place']

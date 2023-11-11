from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from backend import models, serializers
# Create your views here.

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'type']

    company_pk = openapi.Parameter('pk', openapi.IN_QUERY, 
                        description="Id of a company to get details of", 
                        type=openapi.TYPE_INTEGER)
    company_name = openapi.Parameter('name', openapi.IN_QUERY, 
                        description="Name of companies to filter by", 
                        type=openapi.TYPE_STRING)
    company_type = openapi.Parameter('type', openapi.IN_QUERY, 
                        description="Type of companies to filter by", 
                        type=openapi.TYPE_STRING)
    @swagger_auto_schema(responses={400: 'Company id is not a number',
                                    404: 'Invalid company id'},
                         manual_parameters=[company_pk,
                                            company_name,
                                            company_type])
    def retrieve(self, request):
        pk = request.GET.get('pk')
        if not pk:
            return super().list(request)
        if not pk.isdigit():
            return Response("Query parameter 'pk' is not a number", status=400) 
        self.kwargs['pk'] = pk
        return super().retrieve(request)
    
    @swagger_auto_schema(responses={},
                        request_body=serializers.CompanyPutSerializer)
    def update(self, request):
        pk = request.data['pk']
        self.kwargs['pk'] = pk
        return super().update(request)


class TrashComponentViewSet(viewsets.ModelViewSet):
    queryset = models.TrashComponent.objects.all()
    serializer_class = serializers.TrashComponentSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'recyclable', 'mass']

    trashcomponent_pk = openapi.Parameter('pk', openapi.IN_QUERY, 
                        description="Id of a trash component to get details of", 
                        type=openapi.TYPE_INTEGER)
    trashcomponent_name = openapi.Parameter('name', openapi.IN_QUERY, 
                        description="Name of trash components to filter by", 
                        type=openapi.TYPE_STRING)
    trashcomponent_recyclable = openapi.Parameter('recyclable', openapi.IN_QUERY, 
                        description="Recyclability of trash components to filter by", 
                        type=openapi.TYPE_STRING)
    trashcomponent_mass = openapi.Parameter('mass', openapi.IN_QUERY, 
                        description="Mass of trash components to filter by", 
                        type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(responses={400: 'Trash component id is not a number',
                                    404: 'Invalid trash component id'},
                         manual_parameters=[trashcomponent_pk,
                                            trashcomponent_name,
                                            trashcomponent_recyclable,
                                            trashcomponent_mass])
    def retrieve(self, request, **kwargs):
        pk = request.GET.get('pk')
        if not pk:
            return super().list(self, request)
        if not pk.isdigit():
            return Response("Query parameter 'pk' is not a number", status=400) 
        self.kwargs['pk'] = pk
        return super().retrieve(self, request)

    @swagger_auto_schema(responses={},
                        request_body=serializers.TrashComponentPutSerializer)
    def update(self, request):
        pk = request.data['pk']
        self.kwargs['pk'] = pk
        return super().update(request)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'company', 'type']

    product_pk = openapi.Parameter('pk', openapi.IN_QUERY, 
                        description="Id of a product to get details of", 
                        type=openapi.TYPE_INTEGER)
    product_name = openapi.Parameter('name', openapi.IN_QUERY, 
                        description="Name of products to filter by", 
                        type=openapi.TYPE_STRING)
    product_company = openapi.Parameter('company', openapi.IN_QUERY, 
                        description="Id of a company to filter products by", 
                        type=openapi.TYPE_INTEGER)
    product_type = openapi.Parameter('type', openapi.IN_QUERY, 
                        description="Type of products to filter by", 
                        type=openapi.TYPE_STRING)
    @swagger_auto_schema(responses={400: 'Product id is not a number',
                                    404: 'Invalid product id'},
                         manual_parameters=[product_pk,
                                            product_name,
                                            product_company,
                                            product_type])
    def retrieve(self, request, **kwargs):
        pk = request.GET.get('pk')
        if not pk:
            return super().list(self, request)
        if not pk.isdigit():
            return Response("Query parameter 'pk' is not a number", status=400) 
        self.kwargs['pk'] = pk
        return super().retrieve(self, request)

    @swagger_auto_schema(responses={},
                        request_body=serializers.ProductPutSerializer)
    def update(self, request):
        pk = request.data['pk']
        self.kwargs['pk'] = pk
        return super().update(request)


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = models.Receipt.objects.all()
    serializer_class = serializers.ReceiptSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['products', 'time', 'place']

    receipt_pk = openapi.Parameter('pk', openapi.IN_QUERY, 
                        description="Id of a receipt to get details of", 
                        type=openapi.TYPE_INTEGER)
    receipt_time_ge = openapi.Parameter('time_ge', openapi.IN_QUERY, 
                    description="The beginning of a time period of receipts to filter by", 
                        type=openapi.TYPE_STRING)
    receipt_time_le = openapi.Parameter('time_le', openapi.IN_QUERY, 
                        description="The end of a time period of receipts to filter by", 
                        type=openapi.TYPE_STRING)
    receipt_place = openapi.Parameter('place', openapi.IN_QUERY, 
                        description="Id of a company to filter receipts by", 
                        type=openapi.TYPE_INTEGER)
    receipt_type = openapi.Parameter('type', openapi.IN_QUERY, 
                        description="Type of receipts to filter by", 
                        type=openapi.TYPE_STRING)
    @swagger_auto_schema(responses={400: 'Product id is not a number',
                                    404: 'Invalid receipt id'},
                         manual_parameters=[receipt_pk,
                                            receipt_time_ge,
                                            receipt_time_le,
                                            receipt_place,
                                            receipt_type])
    def retrieve(self, request, **kwargs):
        pk = request.GET.get('pk')
        if not pk:
            return super().list(self, request)
        if not pk.isdigit():
            return Response("Query parameter 'pk' is not a number", status=400) 
        self.kwargs['pk'] = pk
        return super().retrieve(self, request)

    @swagger_auto_schema(responses={},
                        request_body=serializers.ProductPutSerializer)
    def update(self, request):
        pk = request.data['pk']
        self.kwargs['pk'] = pk
        return super().update(request)

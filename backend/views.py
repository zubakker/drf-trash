from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password

from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from rest_framework.serializers import CharField
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django_filters.rest_framework import DjangoFilterBackend, DateTimeFilter

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from backend import models, serializers, permissions
# Create your views here.

headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
        }


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
            return Response("Query parameter 'pk' is not a number", status=400, headers=headers) 
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
    serializer_class = serializers.ProductGetSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'company', 'type']
    # permission_classes = [permissions.OwnerOrReadOnly]

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

    @swagger_auto_schema(responses={400: 'Invalid data provided',
                                    401: 'Unauthorized'},
                         request_body=serializers.ProductSerializer,
                         manual_parameters=[permissions.authorization_header])
    def create(self, request):
        self.serializer_class = serializers.ProductSerializer
        return super().create(request)


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = models.Receipt.objects.all()
    serializer_class = serializers.ReceiptGetSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['products', 'place']
    filterset_fields = {
        'time': ['gte', 'lte'],
        'products': ['exact'],
        'place': ['exact'],
        'user': ['exact'],
    }
    permission_classes = [permissions.IsOwnerOrReadOnly]

    receipt_pk = openapi.Parameter('pk', openapi.IN_QUERY, 
                        description="Id of a receipt to get details of", 
                        type=openapi.TYPE_INTEGER)
    receipt_time_ge = openapi.Parameter('time_gte', openapi.IN_QUERY, 
                    description="The beginning of a time period of receipts to filter by", 
                        type=openapi.TYPE_STRING)
    receipt_time_le = openapi.Parameter('time_lte', openapi.IN_QUERY, 
                        description="The end of a time period of receipts to filter by", 
                        type=openapi.TYPE_STRING)
    receipt_place = openapi.Parameter('place', openapi.IN_QUERY, 
                        description="Id of a company to filter receipts by", 
                        type=openapi.TYPE_STRING)
    receipt_user = openapi.Parameter('user', openapi.IN_QUERY, 
                        description="Id of a user to filter receipts by", 
                        type=openapi.TYPE_INTEGER)
    receipt_type = openapi.Parameter('type', openapi.IN_QUERY, 
                        description="Type of receipts to filter by", 
                        type=openapi.TYPE_STRING)
    receipt_stats = openapi.Parameter('stats', openapi.IN_QUERY, 
                        description="Whether the respons needs to contain statistics or not. False by default", 
                        type=openapi.TYPE_BOOLEAN)
    @swagger_auto_schema(responses={400: 'Product id is not a number',
                                    404: 'Invalid receipt id'},
                         manual_parameters=[receipt_pk,
                                            receipt_time_ge,
                                            receipt_time_le,
                                            receipt_place,
                                            receipt_user,
                                            receipt_type,
                                            receipt_stats])
    def retrieve(self, request, **kwargs):
        pk = request.GET.get('pk')
        stats = request.GET.get('stats')
        if not pk:
            queryset = self.filter_queryset(self.get_queryset())
            if stats == 'true':
                serializer_data = self.serializer_class(queryset, many=True,
                                                   context={'request': request}).data
                statistics = dict()
                cum_mass = 0
                for receipt in serializer_data:
                    for product in receipt['products_set']:
                        for component in product['trash_set']:
                            recyclable = component['recyclable']
                            mass = component['mass']
                            cum_mass += mass
                            if recyclable in statistics:
                                statistics[recyclable] += mass
                            else:
                                statistics[recyclable] = mass
                print(statistics)
            result_page = self.paginator.paginate_queryset(queryset, request)
            serializer = self.serializer_class(result_page, many=True,
                                               context={'request': request})

            response = self.paginator.get_paginated_response(serializer.data)
            if stats == 'true':
                response.data['stats'] = statistics
                response.data['cum_mass'] = cum_mass
            # return self.paginator.get_paginated_response(serializer.data)
            return response
            # return super().list(self, request)
        if not pk.isdigit():
            return Response("Query parameter 'pk' is not a number", status=400) 
        self.kwargs['pk'] = pk
        return super().retrieve(self, request)

    @swagger_auto_schema(responses={201: serializers.ReceiptSerializer,
                                    403: 'Trying to update a receipt of another user'},
                         request_body=serializers.ReceiptPutSerializer,
                         manual_parameters=[permissions.authorization_header])
    def update(self, request):
        pk = request.data['pk']
        self.kwargs['pk'] = pk
        return super().update(request)

    @swagger_auto_schema(responses={400: 'Invalid data provided',
                                    401: 'Unauthorized'},
                         request_body=serializers.ReceiptSerializer,
                         manual_parameters=[permissions.authorization_header])
    def create(self, request):
        user = request.user
        if user.is_anonymous:
            return Response('Unauthorized', status=401)
        self.serializer_class = serializers.ReceiptSerializer
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        obj = serializer.save()
        obj.user = request.user
        obj.save()
        return Response(serializer.data, status=201)



class AuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = PageNumberPagination


    @swagger_auto_schema(responses={201: serializers.TokenSerializer,
                                    400: 'Invalid data provided'})
    def register(self, request):
        if 'password' not in list(request.data):
            return Response('Username or password not provided', status=400)
        request.data['password'] = make_password(request.data['password'])
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400, headers=headers)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        return Response({'refresh': str(token),
                         'access': str(token.access_token)}, status=201)
        
    @swagger_auto_schema(responses={200: serializers.TokenSerializer,
                                    400: 'Username or password not provided',
                                    401: 'Wrong password',
                                    404: 'User not found'})
    def login(self, request):
        if 'username' not in list(request.data) or 'password' not in list(request.data):
            return Response('Username or password not provided', status=400)
        user = get_object_or_404(self.queryset, username=request.data['username'])
        if not check_password(request.data['password'], user.password):
            return Response('Wrong password', status=401)
        token = RefreshToken.for_user(user)
        return Response({'refresh': str(token),
                         'access': str(token.access_token)})

    @swagger_auto_schema(responses={200: serializers.TokenSerializer,
                                    400: 'Invalid or expired token'},
                         request_body=serializers.RefreshTokenSerializer)
    def refresh(self, request):
        try:
            token = RefreshToken(request.data['refresh'])
        except TokenError:
            return Response('Invalid or expired token', status=400)

        return Response({'refresh': str(token),
                         'access': str(token.access_token)}, status=200)


class UsersMeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = PageNumberPagination


    @swagger_auto_schema(responses={401: 'Unauthorized or invalid token'},
                         manual_parameters=[permissions.authorization_header])
    def retrieve(self, request):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=401)
        self.kwargs['pk'] = request.user.id
        return super().retrieve(request)
        
    @swagger_auto_schema(responses={400: 'Invalid data provided',
                                    401: 'Unauthorized or invalid token'},
                         manual_parameters=[permissions.authorization_header],
                         request_body=serializers.UserSerializer)
    def update(self, request):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=401)
        self.kwargs['pk'] = request.user.id
        request.data['password'] = make_password(request.data['password'])
        return super().update(request)

    @swagger_auto_schema(responses={204: 'User successfully deleted',
                                    401: 'Unauthorized or invalid token'},
                         manual_parameters=[permissions.authorization_header])
    def destroy(self, request):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=401)
        self.kwargs['pk'] = request.user.id
        return super().destroy(request)


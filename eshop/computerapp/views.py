# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from computerapp.models import Category,Product,Manufacturer,UserProfile,DeliveryAddress,Order
from django.contrib.auth.models import User
from computerapp.serializers import ProductListSerializer,ProductRetrieveSerializer,UserInfoSerializer,UserSerializer,DeliveryAddressSerializer,OrderListSerializer,OrderCreateSerializer
from rest_framework import permissions
from rest_framework import generics
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
import json
import datetime
import logging
LOG_FILENAME = 'shop.log'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBU)
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

# class CategoryList(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    """
    产品列表
    """
    queryset = Product.objects.all()#.order_by('price')
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)#结尾的逗号不能删除，否则会报错： TypeEoore：'BasePermissionMetaclass' object is not iterable
    filter_backends = (OrderingFilter,SearchFilter)#排序
    ordering_fields = ('category','manufacturer','created','price',)#按照括号里的选项排序，可以在页面选择,不写这一行，就会按模型里的地段来选择。
    search_fields = ('model',)
    ordering = ('id')
    pagination_class = LimitOffsetPagination    #可以让前端输入limit参数来控制分页的数量和使用offset来控制初始位置，初始位置默认为0.

class ProductListByCategoryView(generics.ListAPIView):
    """
    产品列表按类别显示
    """
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (OrderingFilter,SearchFilter,)
    ordering_fields = ('category','manufacturer','created','sold','price',)
    search_fields = ('model',)
    ordering = ('id')

    def get_queryset(self):
        category = self.request.query_params.get('category',None)
        if category is not None:
            querset = Product.objects.filter(category=category)
        else:
            querset = Product.objects.all()
        return querset

class ProductListByCategoryManufacturerView(generics.ListAPIView):
    """
    产品按类别按品牌显示
    """
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (OrderingFilter,SearchFilter,)
    ordering_fields = ('category','manufacturer','created','sold','price',)
    search_fields = ('model',)
    ordering = ('id')

    def get_queryset(self):
        category = self.request.query_params.get('category',None)
        manufacturer = self.request.query_params.get('manufacturer', None)
        if category is not None:
            querset = Product.objects.filter(category=category,manufacturer=manufacturer)
        else:
            querset = Product.objects.all()
        return querset

class ProductRetrieveView(generics.RetrieveAPIView):
    """
    产品详情列表
    """
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
    permission_classes = (permissions.AllowAny,)


# class ManufacturerList(generics.ListCreateAPIView):
#     queryset = Manufacturer.objects.all()
#     serializer_class = ManufacturerSerializer
#
#
# class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductListSerializer

class UserInfoView(APIView):
    """
    用户信息
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,format=None):
        user = self.request.user #把当前用户信息返回到变量user
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)

class UserProfileRUView(generics.RetrieveUpdateAPIView):
    """用户其他信息"""
    serializer_class = UserInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_object(self):
        user = self.request.user
        obj = UserProfile.objects.get(user=user)
        return obj

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

class DeliveryAddressLCView(generics.ListCreateAPIView):
    serializer_class = DeliveryAddressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        querset = DeliveryAddress.objects.filter(user=user)
        return querset

    def perform_create(self, serializer):
        user = self.request.user
        s = serializer.save(user=user)
        profile = user.profile_of
        profile.delivery_address = s
        profile.save()

class DeliveryAddressRUDView(generics.RetrieveUpdateDestroyAPIView):
    """
    收货地址RUD
    """
    serializer_class = DeliveryAddressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        try:
            obj = DeliveryAddress.objects.get(id=self.kwargs['pk'],user=user)
        except Exception as e:
            raise NotFound('not found')
        return obj




class CartListView(generics.ListAPIView):
    """
    购物车列表
    """
    serializer_class = OrderListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        querset = Order.objects.filter(user=user,status='0')
        return querset


class OrderListView(generics.ListAPIView):
    """
    订单列表
    """
    serializer_class = OrderListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        user = self.request.user

        querset = Order.objects.filter(user=user,status__in=['1','2','3','4'])

        return querset

class OrderCreateView(generics.CreateAPIView):
    """
    创建订单
    """
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data.get('product')
        serializer.save(user=user,price=product.price,address= self.request.user.profile_of.delivery_address)

        logging.info('user %d cart changed,product %d related. Time is %s.',user.id, product.id, str(datetime.datetime.now()))
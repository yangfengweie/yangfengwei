# -*- coding: utf-8 -*-
from rest_framework import serializers
from computerapp.models import Category,Product,Manufacturer,UserProfile,DeliveryAddress,Order
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id','user','mobile_phone','nickname','description','icon','created','updated',)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','last_name','first_name','email',)
        extra_kwargs = {'password':{'write_only':True}}
    def create(self,validated_data):#在views中使用perform_create，在序列器中使用create，都是在创建的时候运行以下代码
        user = User(**validated_data)#接受经过验证的数据
        user.set_password(validated_data['password'])#使用set_password进行密码加密
        user.save()
        user_profile = UserProfile(user=user)
        user_profile.save()
        return user
class UserInfoSerializer(serializers.ModelSerializer):
    profile_of = UserProfileSerializer()
    class Meta:
        model = User
        fields = ('id','username','email','password','last_login','is_superuser','first_name','last_name',
                  'date_joined','profile_of',)
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields =('id','name','created','updated',)

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('id','name',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name',)

class ProductListSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()#类的名称后面加括号是类的初始化，这句话的意思是把生产商id换成生产商name
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ('id','model','image','price','category','manufacturer',)

class ProductRetrieveSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()  # 类的名称后面加括号是类的初始化，这句话的意思是把生产商id换成生产商name
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ('id','model','image','price','category','manufacturer','description','created','updated',)


# class ManufacturerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Manufacturer
#         fields = ('name','description','logo','created','updated',)
#
#
# class ProductDatilSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Manufacturer
#         fields = ('id','model','image','price','category','manufacturer',)

class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ('id','user','contact_person','contact_mobile_phone','delivery_address','created','updated',)
        read_only_fields = ('user',)


class OrderListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    address = DeliveryAddressSerializer()
    class Meta:
        model = Order
        fields = ('id','user','status','remark','product','price','quantity','address','created','updated',)

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','user','status','remark','product','price','quantity','address','created','updated',)
        read_only_fields = ('user','price','address',)

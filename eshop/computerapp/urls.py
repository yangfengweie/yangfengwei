from django.conf.urls import url
from django.contrib import admin
from computerapp import views

urlpatterns = [
    # url(r'^category_list/$',views.CategoryList.as_view(),name='category_list'),
    url(r'^product_list/$',views.ProductListView.as_view(),name='product_list'),

    # url(r'product_list/(?P<pk>[0-9]+)/$', views.ProductDetail.as_view(), name='product-detail'),
    # url(r'^manufacturerlist/$',views.ManufacturerList.as_view(),name='manufacturer-list'),

    url(r'^product_list_by_category/$',views.ProductListByCategoryView.as_view(),name='product_list_by_category'),

    url(r'^product_list_by_category_manufacturer/$',views.ProductListByCategoryManufacturerView.as_view(),name='product_list_by_category_manufacturer'),

    url(r'^product_retrieve/(?P<pk>[0-9]+)/$',views.ProductRetrieveView.as_view(),name='product_retrieve'),

    url(r'^user_info/$',views.UserInfoView.as_view(),name='user_info'),

    url(r'^user_profile_ru/(?P<pk>[0-9]+)/$',views.UserProfileRUView.as_view(),name='user_profile_ru'),

    url(r'^user_create/$',views.UserCreateView.as_view(),name='user_create'),

    url(r'^delivery_address_lc/$',views.DeliveryAddressLCView.as_view(),name='delivery_address_lc'),

    url(r'^delivery_address_rud/(?P<pk>[0-9]+)/$',views.DeliveryAddressRUDView.as_view(),name='delivery_address_rud'),

    url(r'^cart_list/$',views.CartListView.as_view(),name='cart_list'),

    url(r'^order_list/$',views.OrderListView.as_view(),name='order_list'),

    url(r'^order_create/$',views.OrderCreateView.as_view(),name='order_create'),


]
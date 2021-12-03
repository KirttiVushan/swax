from django.urls import path
from . import views

app_name='shop'

urlpatterns = [
    path('', views.HomeView.as_view() , name='item_list'),
    path('checkout/', views.check_out_item , name='checkout'),
    path('product/<slug>/',views.Product_detail_view.as_view() , name='product_details'),
    path('add_to_cart/<slug>/',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<slug>/',views.remove_from_cart,name='remove_from_cart'),
    path('order_summary', views.OrderSummary.as_view() , name='order_summary'),
    path('remove_single_item/<slug>/',views.remove_single_item_from_cart , name='remove_single_item')
]

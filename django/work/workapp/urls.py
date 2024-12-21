from django.urls import path
from . import views

urlpatterns=[
    path('',views.loginn,name='loginn'),
    path('logout',views.loginn,name='logout'),
    path('index',views.index,name='index'),
    path('apply',views.apply,name='apply'),
    path('user',views.user,name='user'),
    path('newcustomer',views.newcustomer,name='newcustomer'),
    path('searchuser',views.apply,name='searchuser'),
    path('fuelcharge/<int:apply_id>/',views.fuelcharge,name='fuelcharge'),
    path('foodallowance/<int:apply_id>/',views.foodallowance,name='foodallowance'),
    path('itempurchased/<int:apply_id>/',views.itempurchased,name='itempurchased'),
    path('vendorinfo/<int:apply_id>/',views.vendorinfo,name='vendorinfo'),
    path('currentstatus/<int:apply_id>/',views.currentstatus,name='currentstatus'),
    path('updatefuelcharge/<int:fuel_id>/',views.updatefuelcharge,name='updatefuelcharge'),
    path('updatefoodallowance/<int:food_id>/',views.updatefoodallowance,name='updatefoodallowance'),
    path('updateitempurchased/<int:item_id>/',views.updateitempurchased,name='updateitempurchased'),
    path('updatevendorinfo/<int:vendor_id>/',views.updatevendorinfo,name='updatevendorinfo'),
    path('updatecurrentstatus/<int:status_id>/',views.updatecurrentstatus,name='updatecurrentstatus'),
    
]
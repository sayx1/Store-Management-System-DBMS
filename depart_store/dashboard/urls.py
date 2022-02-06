from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='dashboard-index'),
    path('dashboard/', views.index,name='dashboard-index'),
    path('products/', views.products,name='dashboard-products'),
    path('manage/', views.manage,name='dashboard-manage'),
    path('view/', views.view,name='dashboard-view'),
    path('edit/page<int:id>', views.edit,name='dashboard-edit'),
    path('delete/page<int:id>/', views.delete,name='dashboard-delete'),
    path('add/page<int:id>/',views.add,name="dashboard-add"),
    path('delcart/page<int:id>/',views.del_cart,name="dashboard-del_cart"),
    path('checkout/',views.checkout,name="dashboard-checkout"),
]

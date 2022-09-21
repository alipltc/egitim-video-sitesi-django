from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addtocart/<int:id>', views.addtocart, name='addtocart'),
    path('deleteshopcart/<int:id>', views.deleteshopcart, name='deleteshopcart'),
    path('ordervideo/', views.ordervideo, name='ordervideo'),
]
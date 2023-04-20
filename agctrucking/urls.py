from django.urls import path
from . import views

app_name = "agctrucking"

urlpatterns = [
    # path('', views.index, name='index'),
    # path('1', views.openorders_list, name='openorders'),
    path("open-orders", views.main, name="main"),
    path("shipped", views.shipped, name="shipped"),
    path("edit/<ord>", views.edit, name="edit"),
    path("delete/<ord>", views.delete_order, name="delete"),
]

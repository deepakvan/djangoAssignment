from django.contrib import admin
from django.urls import path,include
from .api import RegisterApi
from . import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [

    path('',views.home,name="home"),
    path('api/register', RegisterApi.as_view(),name="register"),

    path('api/addbook',views.AddBook.as_view(), name='AddBook'),
    path('api/updatebook',views.UpdateBook.as_view(), name='UpdateBook'),
    path('api/deletebook',views.DeleteBook.as_view(), name='DeleteBook'),
    path('api/viewbook',views.ViewBook.as_view(), name='ViewBook'),
    path('api/viewallbook',views.ViewAllBook.as_view(), name='ViewAllBook'),

    path('api/borrowbook',views.BorrowBook.as_view(), name='BorrowBook'),
    path('api/returnbook',views.ReturnBook.as_view(), name='ReturnBook'),

    path('api/addmember', views.AddMember.as_view(), name='AddMember'),
    path('api/updatemember', views.UpdateMember.as_view(), name='UpdateMember'),
    path('api/deletemember', views.DeleteMember.as_view(), name='DeleteMember'),
    path('api/viewmember', views.ViewMember.as_view(), name='ViewMember'),
    path('api/viewallmember', views.ViewAllMember.as_view(), name='ViewAllMember'),

    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]

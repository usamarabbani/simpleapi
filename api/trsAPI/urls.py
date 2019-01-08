"""trsAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from trsAPI.reviews import api as reviews_api

schema_view = get_swagger_view(title='Reviews API')

router = DefaultRouter()
router.register(r'users', reviews_api.UserViewSet, basename='user')
router.register(r'companies', reviews_api.CompanyViewSet, basename='company')
router.register(r'reviews', reviews_api.ReviewViewSet, basename='review')

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    re_path(r'^api-token-auth/', views.obtain_auth_token),
    re_path(r'^api/docs/$', schema_view)
]

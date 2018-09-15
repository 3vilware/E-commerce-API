"""ecomerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from EAPI import serilizer

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^createUser/$', serilizer.createUser, name="createUser"),
    url(r'^loguin/$', serilizer.login, name="login"),
    url(r'^createProduct/$', serilizer.createProduct, name="createProduct"),
    url(r'^getProduct/(?P<id>\w+)/$', serilizer.getProduct, name="getProduct"),
    url(r'^getProductByName/(?P<name>\w+)/$', serilizer.getProductByName, name="getProductByName"),
    url(r'^getAllProducts/(?P<orderby>\w+)$', serilizer.getAllProducts, name="getAllProducts"),
    url(r'^updateProductPrice/$', serilizer.updateProductPrice, name="updateProductPrice"),
    url(r'^deleteProduct/$', serilizer.deleteProduct, name="deleteProduct"),
    url(r'^likeProduct/$', serilizer.likeProduct, name="likeProduct"),
    url(r'^buyProduct/$', serilizer.buyProduct, name="buyProduct"),
    url(r'^salesLog/$', serilizer.salesLog, name="salesLog"),

]

from django.conf.urls import url
from django.contrib import admin
from EAPI import serilizer

app_name = "EAPI"

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
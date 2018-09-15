from django.conf.urls import url, include
from django.contrib import admin
from EAPI import serilizer

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('EAPI.urls')),
]

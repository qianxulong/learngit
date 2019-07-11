"""advance URL Configuration

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
from app01 import views as v1
from app02 import views as v2
from app03 import views as v3

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'/appp01/login/', v1.login),
    url(r'transfer/', v1.transfer),
    url(r'book/', v1.page),
    url(r'^page/', v2.page),
    url(r'^log/', v2.login),
    url(r'^app02/display/', v2.display),
    url(r'^login/', v3.login),
    url(r'^display/', v3.display),
    url(r'^logout/', v3.logout),
    url(r'^userinfo/', v3.UserInfo.as_view()),
    url(r'^index/', v2.index),
    url(r'^check1/', v2.check1),
    url(r'^check2/', v2.check2),
    url(r'^reg2/', v2.reg2),

]

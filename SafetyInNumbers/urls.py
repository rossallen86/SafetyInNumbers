"""SafetyInNumbers URL Configuration

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
from django.urls import path
from django.conf.urls import url, include
from safety_in_numbers.views import Index, Profile, CreateTransit, MyTransits, JoinTransits

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='Index'),
    url(r'^accounts/', include('allauth.urls')),
    url('^accounts/profile/', Profile.as_view(), name='Profile'),
    url(r'^transit/create_transit/', CreateTransit.as_view(), name='Create_Transit'),
    url(r'^transit/my_transits/', MyTransits.as_view(), name='My_Transits'),
    url(r'^delete/(?P<part_id>[0-9]+)/$', MyTransits.delete, name='delete_transit'),
    url(r'^transit/join_transits/', JoinTransits.as_view(), name='Join_Transits'),
    url(r'^join/(?P<part_id>[0-9]+)/$', JoinTransits.join, name='join_transit'),
]

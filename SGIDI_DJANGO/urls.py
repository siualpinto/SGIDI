"""SGIDI_DJANGO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
import notifications.urls

from sgidi import views

urlpatterns = [
    # url(r'^login/$', views.login_user, name='login'),
    url(r'^user/', include('sgidi.urls')),
    url(r'^login/$', auth_views.LoginView, name='login'),
    url(r'^logout/$', auth_views.LogoutView, {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^', include('sgidi.urls')),
]
admin.site.site_header = 'Nibble - SGIDI - administration'

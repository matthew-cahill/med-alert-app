"""
URL configuration for med_alert_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from med_alert_app import views
from med_alert_project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('med_alert_app.urls')),
    path('', include('social.apps.django_app.urls', namespace='social'))
]
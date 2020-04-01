"""phishtray URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url, include
from django.urls import path
from django.views.generic import TemplateView

from phishtray import settings

admin.site.site_header = "Phishtray Administration"

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="index.html"), name="index"),
    url(r"^welcome/", TemplateView.as_view(template_name="index.html"), name="index"),
    url(r"^api/v1/", include("phishtray.api_urls")),
    url(r"^admin/", admin.site.urls),
    url(r"^api-auth/", include("rest_framework.urls")),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

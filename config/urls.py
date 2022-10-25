"""odn_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularSwaggerView
from drf_spectacular.views import SpectacularJSONAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('devices/', include('device.urls'),),
    path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("", SpectacularSwaggerView.as_view(url_name="schema-json"),
         name="swagger-ui",)

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.site_header = 'ODN API ADMIN'
admin.site.site_title = 'ODN API ADMIN'

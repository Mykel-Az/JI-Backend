"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
# import accounts
# from accounts.routers import *
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/accounts/', include('accounts.urls')),
    # path('api/v1/trades/', include('trades_services.urls')),
    # path('api/v1/jobs/', include('Jobs.urls')),
    # path('api/v1/professionals/', include('professionals.urls')),
    path('api/v1/companies/', include('company.urls')),

    # Swagger and schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger_ui'),
]

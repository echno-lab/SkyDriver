"""
URL configuration for skydriver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from rest_framework_simplejwt.views import TokenRefreshView

from api import urls as api_urls
from api.user.views import MyTokenObtainPairView
from flight import urls as flight_urls
from user import urls as user_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__reload__", include("django_browser_reload.urls")),
    path("", include(flight_urls)),
    path("", include(user_urls)),
    path("api/", include(api_urls)),
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

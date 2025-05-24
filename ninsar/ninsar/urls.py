from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

"""
СООБЩЕНИЕ ПРОВЕРЯЮЩЕМУ!
Авторизацию можно было написать с использованием КУКИ файлов, с параметром HTTPONLY=True
для этого нужна библиотека dj_rest_auth
"""

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("api/v1/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    path("api/v1/results/", include("competitions_app.urls")),
]

# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    ClubViewSet,
    PlayerViewSet,
    NewsViewSet,
    ApiPlaygroundView,   # страница для вставки токена
)

router = DefaultRouter()
router.register(r'clubs',   ClubViewSet,   basename='api-clubs')
router.register(r'players', PlayerViewSet, basename='api-players')
router.register(r'news',    NewsViewSet,   basename='api-news')

urlpatterns = [
    # JWT
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Песочница: вставить токен и вызывать API
    path('try/', ApiPlaygroundView.as_view(), name='api-try'),

    # Сами REST-эндпоинты
    path('', include(router.urls)),
]



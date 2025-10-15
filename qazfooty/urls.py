from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

# Главная часть (как было)
from clubs import views as clubs_views

# --- Swagger: пытаемся drf_yasg → если нет, пробуем drf-spectacular → если нет, без Swagger ---
swagger_urls = []
try:
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from rest_framework import permissions

    schema_view = get_schema_view(
        openapi.Info(
            title="QazFooty API",
            default_version="v1",
            description="Документация API (JWT)",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    swagger_urls = [
        re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
        path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]
except Exception:
    try:
        from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
        swagger_urls = [
            path("schema/", SpectacularAPIView.as_view(), name="schema"),
            path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="schema-swagger-ui"),
            path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="schema-redoc"),
        ]
    except Exception:
        swagger_urls = []

urlpatterns = [
    path("admin/", admin.site.urls),

    # Веб-страницы
    path("", clubs_views.home, name="home"),
    path("clubs/", clubs_views.clubs_all, name="clubs_all"),
    path("club/<int:pk>/", clubs_views.club_detail, name="club_detail"),
    path("search/", clubs_views.search, name="search"),
    path("news/", clubs_views.news_list, name="news_list"),

    # Users (namespace)
    path("users/", include(("users.urls", "users"), namespace="users")),

    # API (токены в api/urls.py)
    path("api/", include("api.urls")),
] + swagger_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)










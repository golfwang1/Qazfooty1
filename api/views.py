from rest_framework import viewsets, permissions
from clubs.models import Club, Player, News
from .serializers import ClubSerializer, ClubDetailSerializer, PlayerSerializer, NewsSerializer
from django.views.generic import TemplateView

class ClubViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Club.objects.all().order_by("id")
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ClubDetailSerializer
        return ClubSerializer


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Player.objects.select_related("club").all().order_by("id")
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/news/       -> список новостей (нужен токен)
    GET /api/news/{id}/  -> детально (нужен токен)
    """
    queryset = News.objects.all().order_by("-published_at")  # ✅ исправили
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

class ApiPlaygroundView(TemplateView):
    """
    Простая страничка, где пользователь вставляет JWT access-token
    и может выполнять запросы к /api/clubs/, /api/players/, /api/news/.
    """
    template_name = "api/playground.html"


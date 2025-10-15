from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from .models import Club, Player, News


def home(request):
    """
    Главная: свежие новости, топ клубов, группы.
    """
    news = (
        News.objects
        .filter(is_published=True)
        .order_by("-published_at")[:7]
    )
    clubs = Club.objects.all().order_by("name")[:6]
    groups = (
        Group.objects
        .annotate(members_count=Count("user"))
        .order_by("name")[:6]
    )
    return render(request, "clubs/home.html", {
        "news": news,
        "clubs": clubs,
        "groups": groups,
    })


def clubs_all(request):
    clubs = Club.objects.all().order_by("name")
    return render(request, "clubs/clubs_all.html", {"clubs": clubs})


def club_detail(request, pk: int):
    club = get_object_or_404(Club, pk=pk)
    return render(request, "clubs/club_detail.html", {"club": club})


def search(request):
    q = (request.GET.get("q") or "").strip()
    clubs = players = users = groups = []
    if q:
        clubs = Club.objects.filter(
            Q(name__icontains=q) | Q(city__icontains=q)
        ).order_by("name")[:50]
        players = Player.objects.filter(
            Q(name__icontains=q) |
            Q(position__icontains=q) |
            Q(club__name__icontains=q)
        ).select_related("club").order_by("name")[:50]
        users = User.objects.filter(
            Q(username__icontains=q) | Q(email__icontains=q)
        ).order_by("username")[:50]
        groups = Group.objects.filter(
            name__icontains=q
        ).annotate(members_count=Count("user")).order_by("name")[:50]

    return render(request, "search/results.html", {
        "q": q,
        "clubs": clubs,
        "players": players,
        "users": users,
        "groups": groups,
    })


def news_list(request):
    """
    Список всех опубликованных новостей с пагинацией.
    """
    items = News.objects.filter(is_published=True).order_by("-published_at")
    paginator = Paginator(items, 10)
    page_obj = paginator.get_page(request.GET.get("page") or 1)

    return render(request, "clubs/news_list.html", {
        "page_obj": page_obj,
        "news": page_obj.object_list,
    })

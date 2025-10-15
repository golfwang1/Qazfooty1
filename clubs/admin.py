# clubs/admin.py
from django.contrib import admin
from .models import Club, Player, News


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "city")


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "club")
    list_filter = ("club",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "published_at")
    list_filter = ("is_published",)
    search_fields = ("title", "excerpt", "body")


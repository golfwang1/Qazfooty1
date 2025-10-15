from django.contrib import admin
from django.contrib.auth.models import Group as AuthGroup
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from .models import GroupProfile, FanPhoto

@admin.register(FanPhoto)
class FanPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "caption", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("caption", "user__username")

class GroupProfileInline(admin.StackedInline):
    model = GroupProfile
    fk_name = "group"
    extra = 0
    max_num = 1
    can_delete = True
    fields = ("club", "avatar", "cover", "photo", "description", "meet_place")

@admin.register(GroupProfile)
class GroupProfileAdmin(admin.ModelAdmin):
    list_display = ("group", "club")
    search_fields = ("group__name", "club__name")

class GroupAdmin(DjangoGroupAdmin):
    inlines = [GroupProfileInline]
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        profiles = GroupProfile.objects.filter(group=form.instance).order_by("id")
        if profiles.count() > 1:
            for p in profiles[1:]:
                p.delete()

admin.site.unregister(AuthGroup)
admin.site.register(AuthGroup, GroupAdmin)




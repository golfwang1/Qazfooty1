from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db.models import Count
from django.conf import settings

from .forms import RegisterForm, FanPhotoForm, UpdateUserForm
from .models import FanPhoto, GroupProfile
from clubs.models import News


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users:profile")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    edit_mode = request.GET.get("edit") == "1"
    uform = UpdateUserForm(instance=request.user)
    pform = FanPhotoForm()

    if request.method == "POST":
        edit_mode = True
        if "update_profile" in request.POST:
            uform = UpdateUserForm(request.POST, instance=request.user)
            if uform.is_valid():
                uform.save()
                return redirect("users:profile")

        if "upload_photo" in request.POST:
            pform = FanPhotoForm(request.POST, request.FILES)
            if pform.is_valid():
                obj = pform.save(commit=False)
                obj.user = request.user
                obj.save()
                return redirect("users:profile")

    my_groups = list(request.user.groups.all().order_by("name"))
    profiles = {p.group_id: p for p in GroupProfile.objects.filter(group__in=my_groups)}
    for g in my_groups:
        g.profile = profiles.get(g.id)

    photos = FanPhoto.objects.filter(user=request.user).order_by("-created_at")
    avatar_photo = photos.first()
    news = News.objects.filter(is_published=True).order_by("-published_at")[:6]

    return render(request, "users/profile.html", {
        "edit_mode": edit_mode,
        "uform": uform,
        "pform": pform,
        "me": request.user,
        "my_groups": my_groups,
        "photos": photos,
        "avatar_photo": avatar_photo,
        "news": news,
    })


@login_required
def users_list(request):
    users = User.objects.all().order_by("username")
    return render(request, "users/users_list.html", {"users": users})


def public_profile(request, username):
    owner = get_object_or_404(User, username=username)
    photos = FanPhoto.objects.filter(user=owner).order_by("-created_at")
    return render(request, "users/public_profile.html", {"profile_user": owner, "photos": photos})


@require_POST
def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def groups_list(request):
    groups = Group.objects.annotate(members_count=Count("user")).order_by("name")
    profiles = {p.group_id: p for p in GroupProfile.objects.filter(group__in=groups)}
    for g in groups:
        g.profile = profiles.get(g.id)
    return render(request, "users/groups_list.html", {"groups": groups})


def group_detail(request, pk: int):
    group = get_object_or_404(Group, pk=pk)
    gp = GroupProfile.objects.filter(group=group).first()

    members = User.objects.filter(groups=group).order_by("username")[:12]
    member_count = User.objects.filter(groups=group).count()
    is_member = request.user.is_authenticated and request.user.groups.filter(id=group.id).exists()

    hero = None
    avatar_ui = None
    if gp:
        hero = getattr(gp, "cover", None) or getattr(gp, "photo", None) or getattr(gp, "avatar", None)
        avatar_ui = getattr(gp, "avatar", None) or getattr(gp, "photo", None)

    return render(request, "users/group_detail.html", {
        "group": group,
        "gp": gp,
        "members": members,
        "member_count": member_count,
        "is_member": is_member,
        "hero": hero,
        "avatar_ui": avatar_ui,
    })


@require_POST
@login_required
def group_join(request, pk: int):
    group = get_object_or_404(Group, pk=pk)
    request.user.groups.add(group)
    messages.success(request, f"Вы присоединились к группе «{group.name}».")
    return redirect("users:group_detail", pk=pk)


@require_POST
@login_required
def group_leave(request, pk: int):
    group = get_object_or_404(Group, pk=pk)
    request.user.groups.remove(group)
    messages.success(request, f"Вы вышли из группы «{group.name}».")
    return redirect("users:group_detail", pk=pk)




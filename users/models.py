# users/models.py
from django.db import models
from django.contrib.auth.models import User, Group

# Если ссылаемся на Club из приложения clubs:
# (импорт по строке во избежание циклов)
# "clubs.Club" в ForeignKey ниже

# ---------- helpers: upload paths ----------
def group_avatar_upload_to(instance, filename):
    # instance: GroupProfile
    return f"groups/{instance.group_id}/avatar/{filename}"

def group_photo_upload_to(instance, filename):
    return f"groups/{instance.group_id}/photo/{filename}"

def group_cover_upload_to(instance, filename):
    return f"groups/{instance.group_id}/cover/{filename}"


# ---------- Пользовательские фан-фото ----------
class FanPhoto(models.Model):
    """
    Фан-фото пользователя (для профиля).
    ВНИМАНИЕ: поле называется photo — под шаблоны/формы, где используется pform.photo и avatar_photo.photo
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="fan_photos",
        verbose_name="Пользователь",
    )
    photo = models.ImageField("Фото", upload_to="fan_photos/")  # <-- photo (не image)
    caption = models.CharField("Подпись", max_length=255, blank=True)
    created_at = models.DateTimeField("Загружено", auto_now_add=True)

    class Meta:
        verbose_name = "Фан-фото"
        verbose_name_plural = "Фан-фото"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} — {self.caption or 'Фото'}"


# ---------- Профиль фан-группы (расширяет auth.Group) ----------
class GroupProfile(models.Model):
    """
    Доп.инфа для фан-группы (строгая 1-к-1 связь с auth.Group).
    НИКАКИХ сигналов post_save — чтобы админский inline не создавал дубли.
    """
    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Группа (auth.Group)",
        unique=True,  # явный unique для читаемости (OneToOne и так уникален)
    )

    # Привязка к клубу (по строке, чтобы не ловить циклические импорты)
    club = models.ForeignKey(
        "clubs.Club",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fan_groups",
        verbose_name="Клуб",
    )

    # Медиа
    cover = models.ImageField("Обложка", upload_to=group_cover_upload_to, blank=True, null=True)
    avatar = models.ImageField("Аватар", upload_to=group_avatar_upload_to, blank=True, null=True)
    photo = models.ImageField("Фото/баннер", upload_to=group_photo_upload_to, blank=True, null=True)

    # Текстовые поля (под шаблоны)
    description = models.TextField("Описание", blank=True)
    meet_place = models.CharField("Место встречи", max_length=255, blank=True)

    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Профиль группы"
        verbose_name_plural = "Профили групп"
        ordering = ["group__name"]

    def __str__(self):
        return f"Профиль: {self.group.name}"


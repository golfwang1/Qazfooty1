from django.db import models
class Club(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    founded = models.PositiveIntegerField(null=True, blank=True)
    titles = models.TextField(blank=True)
    logo = models.ImageField(upload_to='clubs/', blank=True, null=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name
class Player(models.Model):
    name = models.CharField(max_length=120)
    position = models.CharField(max_length=60, blank=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='players')
    photo = models.ImageField(upload_to='players/', blank=True, null=True)
    achievements = models.TextField(blank=True)
    def __str__(self):
        return f"{self.name} ({self.club.name})"
# --- НОВОЕ: простая модель новостей ---
class News(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    excerpt = models.TextField("Короткое описание", blank=True)
    image = models.ImageField("Обложка", upload_to="news/", blank=True, null=True)
    source_url = models.URLField("Ссылка на источник", blank=True)
    published_at = models.DateTimeField("Дата публикации", auto_now_add=True)
    is_published = models.BooleanField("Публиковать", default=True)
    class Meta:
        ordering = ["-published_at"]
    def __str__(self):
        return self.title

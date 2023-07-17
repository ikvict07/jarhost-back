from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, FileExtensionValidator

from django.db import models
from django.utils.text import slugify


class Squad(models.Model):
    name = models.CharField(max_length=70, unique=True, verbose_name='Назва підрозділу')
    description = models.TextField(help_text="Напішіть про ваш підрозділ", verbose_name="Про підрозділ",
                                   error_messages={'blank': "Це поле не може бути пустим"})

    def __str__(self):
        return self.name


class News(models.Model):
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE, related_name='news')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=200, help_text="Назвіть вашу новину",
                             verbose_name="Ваші новини")  # What about validators?
    content = models.TextField(help_text="В цьому полі можете додати новину про ваш підрозділ",
                               verbose_name="Поле для новин")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
        self.slug = slugify(f'{self.title}-{self.id}')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=200, verbose_name="Ваш коментар")  # Need to add validator
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Author does`t have attribute username
    def __str__(self):
        return f'Comment by {self.author.username}'  # Need to check class User, must be field with username
        # or we can to use django.contrib.auth.models.User


def get_upload_to(instance, filename):
    return f'images/{instance.news.author.username}/{filename}'


# Add date validation to upload rules
class Image(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_to,
                              validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    description = models.TextField(blank=True)
    # uploaded_at = models.DateTimeField(auto_now_add=True)                    # Protect user from load images with date
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE, related_name='images', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Фото для новини {self.news.title}' if self.news else f'Відео для підрозділу {self.squad.name}'


def validate_youtube_url(value):
    parsed = urlparse(value)
    if "youtube" not in parsed.netloc.lower():
        raise ValidationError("Це не дійсна URL-адреса YouTube")


# Add date validation to upload rules
class Video(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.URLField(validators=[URLValidator(), validate_youtube_url])
    description = models.TextField(blank=True)
    # uploaded_at = models.DateTimeField(auto_now_add=True)                    # Protect user from load images with date
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Відео для новин {self.news.title}' if self.news else f'Відео для підрозділу {self.squad.name}'

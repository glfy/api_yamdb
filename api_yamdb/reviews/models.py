from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = [
        ("admin", "Administrator"),
        ("moderator", "Moderator"),
        ("user", "User"),
    ]
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    username = models.CharField(
        "Имя пользователя", max_length=150, null=True, unique=True
    )
    email = models.EmailField(
        "Электронная почта",
        max_length=254,
        unique=True,
    )
    bio = models.TextField(
        "Биография",
        null=True,
        blank=True,
    )
    role = models.CharField(
        "Роль пользователя",
        blank=True,
        max_length=100,
        choices=ROLES,
        default="user",
    )

    class Meta:
        verbose_name = "Пользователи"

        # constraints = []
        def __str__(self):
            return self.username


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, related_name="genre")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="categories"
    )

    class Meta:
        verbose_name = "Заголовок"
        verbose_name_plural = "Заголовки"


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    text = models.TextField(blank=False, verbose_name="Текст")
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации отзыва"
    )
    rate = models.IntegerField()

    title = models.ForeignKey(
        Title,
        on_delete=models.PROTECT,
        related_name="reviews",
        verbose_name="Название произведения",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        # constraints = [
        #  models.UniqueConstraint
        ordering = ("-pub_date",)


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата публикации комментария", auto_now_add=True
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

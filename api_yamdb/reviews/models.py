from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username, validate_year


class User(AbstractUser):
    class UserRole(models.TextChoices):
        USER = "user", "User"
        ADMIN = "admin", "Administrator"
        MODERATOR = "moderator", "Moderator"

    first_name = models.CharField(
        max_length=150, null=True, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=150, null=True, verbose_name="Фамилия"
    )
    username = models.CharField(
        "Имя пользователя",
        max_length=150,
        null=True,
        unique=True,
        validators=[
            validate_username,
        ],
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
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    @property
    def is_moderator(self):
        return self.role == self.UserRole.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN

    class Meta:
        verbose_name = "Пользователи"
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="username_is_not_me",
            )
        ]

        def __str__(self):
            return self.username


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название категории")
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name="Слаг категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name} {self.name}"


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название жанра")
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name="Слаг жанра"
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return f"{self.name} {self.name}"


class Title(models.Model):
    name = models.CharField(
        max_length=256, verbose_name="Название произведения"
    )
    year = models.PositiveIntegerField(
        verbose_name="Год", validators=(validate_year,)
    )
    description = models.TextField(
        max_length=256, blank=True, verbose_name="Описание произведения"
    )
    genre = models.ManyToManyField(
        Genre, related_name="genre", verbose_name="Жанр"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        null=True,
        blank=True,
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "Заголовок"
        verbose_name_plural = "Заголовки"

    def __str__(self):
        return self.name


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
    score = models.IntegerField(
        verbose_name="Рейтинг",
        validators=[
            MinValueValidator(1, "Допустимы значения от 1 до 10"),
            MaxValueValidator(10, "Допустимы значения от 1 до 10"),
        ],
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Название произведения",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="unique follow",
            )
        ]
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    text = models.CharField(max_length=200, verbose_name="Текст комментария")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    pub_date = models.DateTimeField(
        "Дата публикации комментария",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text

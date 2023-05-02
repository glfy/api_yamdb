from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator
from django.db.models.signals import post_save


class User(AbstractUser):
<<<<<<< HEAD
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = "user"
=======
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97
    ROLES = [
        (ADMIN, "Administrator"),
        (MODERATOR, "Moderator"),
        (USER, "User"),
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

    @property
<<<<<<< HEAD
    def is_moderator(self):
        return self.role == self.MODERATOR
=======
    def is_user(self):
        return self.role == self.USER
>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97

    @property
    def is_admin(self):
        return self.role == self.ADMIN

<<<<<<< HEAD
=======
    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97
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
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None
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
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        ])
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Название произведения",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique follow',
            )
        ]
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

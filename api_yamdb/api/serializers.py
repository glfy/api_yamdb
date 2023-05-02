from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from reviews.models import User, Category, Genre, Title, Comment, Review


<<<<<<< HEAD
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
=======
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97
        model = User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
<<<<<<< HEAD
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
=======
        fields = "__all__"
        model = Category
        lookup_field = "slug"
>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
<<<<<<< HEAD
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
=======
        fields = "__all__"
        lookup_field = "slug"
>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
<<<<<<< HEAD
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
=======
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97
    )

    class Meta:
        model = Title
<<<<<<< HEAD
        fields = '__all__'
=======
        fields = "__all__"
>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
<<<<<<< HEAD
        slug_field='username',
    )
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text',
    )
    class Meta:
        fields = '__all__'
=======
        slug_field="username",
    )
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field="text",
    )

    class Meta:
        fields = "__all__"
>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
<<<<<<< HEAD
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
=======
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )

    def validate(self, data):
        request = self.context["request"]
        author = request.user
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST":
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    "Вы не можете добавить более"
                    "одного отзыва на произведение"
                )
>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97
        return data

    class Meta:
        model = Review
<<<<<<< HEAD
        fields = '__all__'
=======
        fields = "__all__"
>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
<<<<<<< HEAD
        source='reviews__score__avg', read_only=True
=======
        source="reviews__score__avg", read_only=True
>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
<<<<<<< HEAD
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Username 'me' is not valid")
        return value

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
=======
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97

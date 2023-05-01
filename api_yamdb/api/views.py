
from django.core.mail import send_mail,EmailMessage
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.views import APIView
from rest_framework import permissions,status
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import viewsets, filters
from reviews.models import Genre, Category, Title, User, Review, Comment
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg


from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializer,
    SignUpSerializer,
    GetTokenSerializer,
    UsersSerializer,
)


from .permissions import AdminOnly
from reviews.models import User
import six


class UpdateUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        user = request.user
        serializer = UsersSerializer(
            user, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APISignUp(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = default_token_generator.make_token(user)
        email= EmailMessage(
            subject='Confirmation code',
            body=f'Your confirmation code:{token}',
            to=[user.email]
        )

        email.send()
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        confirmation_code = data.get('confirmation_code')
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if default_token_generator.check_token(user, confirmation_code):
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)

class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    # permission_classes
    queryset = Genre.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
    ]
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    # permission_classes
    queryset = Category.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
    ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    # permission_classes =
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["category__slug", "genre__slug", "name", "year"]
    search_fields = [
        "name",
    ]

    def get_queryset(self):
        queryset = Title.objects.all().annotate(Avg("reviews__rate"))

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAdminUser | IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "username",
    ]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    # permission_classes =
    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)

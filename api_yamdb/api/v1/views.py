from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from api.v1.permissions import (
    AdminModeratorAuthorOrReadOnly,
    AdminOnly,
    AdminOrReadOnly,
)
from reviews.models import Category, Genre, Review, Title, User, Comment

from api.v1.filters import TitleFilter
from api.v1.mixins import CreateDestroyListMixinSet
from api.v1.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    NotAdminSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleSerializer,
    UserSerializer,
    UsersSerializer,
)


class UpdateUserAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def patch(self, request):
        user = request.user
        serializer = UsersSerializer(user, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class APISignUp(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get_or_create(
                email=serializer.validated_data["email"],
                username=serializer.validated_data["username"],
            )
        except IntegrityError:
            raise ValidationError(
                "Неуникальное поле." "Пользователь с таким уже существует"
            )
        user = get_object_or_404(
            User, username=serializer.validated_data["username"]
        )
        token = default_token_generator.make_token(user)
        email = EmailMessage(
            subject="Confirmation code",
            body=f"Your confirmation code:{token}",
            to=[user.email],
        )

        email.send()

        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(
            User,
        )
        confirmation_code = data.get("confirmation_code")
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {"token": str(token)}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"confirmation_code": "Неверный код подтверждения!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GenreViewSet(CreateDestroyListMixinSet):
    serializer_class = GenreSerializer
    permission_classes = [
        AdminOrReadOnly,
    ]
    queryset = Genre.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
    ]
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination


class CategoryViewSet(CreateDestroyListMixinSet):
    serializer_class = CategorySerializer
    permission_classes = [
        AdminOrReadOnly,
    ]
    queryset = Category.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
    ]
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects
        .select_related("category")
        .prefetch_related("genre")
        .annotate(rating=Avg("reviews__score"))
        .all()
    )
    permission_classes = [
        AdminOrReadOnly,
    ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TitleFilter
    search_fields = [
        "name",
    ]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TitleReadSerializer
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated,
        AdminOnly,
    ]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "username",
    ]
    lookup_field = "username"
    http_method_names = ["get", "post", "patch", "delete"]

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=[
            IsAuthenticated,
        ],
        url_path="me",
    )
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == "PATCH":
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user, data=request.data, partial=True
                )
            else:
                serializer = NotAdminSerializer(
                    request.user, data=request.data, partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        AdminModeratorAuthorOrReadOnly,
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Review.objects.select_related('author').filter(
            title=self.kwargs.get("title_id")
        )

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        AdminModeratorAuthorOrReadOnly,
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Comment.objects.select_related('author').filter(
            review=self.kwargs.get("review_id")
        )

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)

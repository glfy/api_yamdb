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
)


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

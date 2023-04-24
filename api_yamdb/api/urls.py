from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import (
    GenreViewSet,
    CategoryViewSet,
    TitleViewSet,
    UserViewSet,
    ReviewViewSet,
    CommentViewSet,
)


router_v1 = DefaultRouter()
router_v1.register(r"genres", GenreViewSet, basename="genres")
router_v1.register(r"categories", CategoryViewSet, basename="categories")
router_v1.register(r"titles", TitleViewSet, basename="titles")
router_v1.register(r"users", UserViewSet, basename="users")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    # path('v1/auth/', include
    path("v1/", include(router_v1.urls))
]

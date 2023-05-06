from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.v1.views import (
    APIGetToken,
    APISignUp,
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
)

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register(r"genres", GenreViewSet, basename="genres")
router_v1.register("categories", CategoryViewSet, basename="categories")
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
    path("v1/auth/signup/", APISignUp.as_view(), name="signup"),
    path("v1/auth/token/", APIGetToken.as_view(), name="get_token"),
    path("v1/", include(router_v1.urls)),
]

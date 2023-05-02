from django.urls import include, path

<<<<<<< HEAD
from rest_framework.routers import DefaultRouter

from api.views import (
=======


from .views import (
    APISignUp,
    APIGetToken,
>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97
    GenreViewSet,
    CategoryViewSet,
    TitleViewSet,
    UserViewSet,
    ReviewViewSet,
    CommentViewSet,
    register,
    get_jwt_token,
)

app_name = 'api'
<<<<<<< HEAD
=======

>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97

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
<<<<<<< HEAD
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_jwt_token, name='token'),
    path("v1/", include(router_v1.urls)),
=======
    path('v1/auth/signup/', APISignUp.as_view(), name='signup'),
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path("v1/", include(router_v1.urls))
>>>>>>> 642c0042ff7db187b170eb471443adf2c8ecde97
]

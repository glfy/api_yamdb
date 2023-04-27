from django.core.mail import send_mail,EmailMessage
from rest_framework import viewsets
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.views import APIView
from rest_framework import permissions,status
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .serializers import SignUpSerializer,GetTokenSerializer
from reviews.models import User
import six


# class APIGetToken(APIView):
#     def post(self, request):
#         serializer = GetTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = serializer.validated_data
#         try:
#             user = User.objects.get(username=data['username'])
#         except User.DoesNotExist:
#             return Response(
#                 {'username': 'Пользователь не найден!'},
#                 status=status.HTTP_404_NOT_FOUND)
#         if default_token_generator.check_token(user, confirmation_code)
#             return Response({'token': str(token)},
#                             status=status.HTTP_201_CREATED)
#         return Response(
#             {'confirmation_code': 'Неверный код подтверждения!'},
#             status=status.HTTP_400_BAD_REQUEST)


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



class GenreViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass

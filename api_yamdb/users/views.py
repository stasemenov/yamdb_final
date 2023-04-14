from api.permissions import IsAdmin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL

from .models import User
from .serializers import (MeSerializer, RegistrationSerializer,
                          TokenSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdmin,)

    @action(methods=['get', 'patch'], detail=False,
            url_path='me', permission_classes=(permissions.IsAuthenticated,))
    def me_user(self, request):
        user = User.objects.get(username=request.user)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        serializer = MeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class RegistrationViewSet(
        mixins.CreateModelMixin, viewsets.GenericViewSet):

    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = RegistrationSerializer(data=request.data)
        email = request.data.get('email')
        username = request.data.get('username')
        if User.objects.filter(username=username, email=email):
            user = User.objects.get(username=username)
            serializer = RegistrationSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=username)
            send_mail('Your confirmation code',
                      f'Ваш код подтверждения: {user.confirmation_code}',
                      DEFAULT_FROM_EMAIL,
                      [email],
                      fail_silently=False)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class TokenViewSet(viewsets.ViewSet):

    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=request.data.get('username'))
            if str(user.confirmation_code) == request.data.get(
                    'confirmation_code'):
                return Response(
                    {'token': str(RefreshToken.for_user(user).access_token)},
                    status.HTTP_200_OK)
            return Response(
                'Проверьте username и confirmation_code',
                status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

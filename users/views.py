from __future__ import unicode_literals

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth import login, logout

from .serializers import UserSerializer
from .forms import AuthenticationForm
from .models import User


class UserAPIView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post'], detail=False)
    def registration(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.data)
        if form.is_valid():
            user = form.get_user()
            if user != request.user:
                logout(request)
            login(request, user)
            return Response()
        else:
            return Response(form.errors, status=HTTP_400_BAD_REQUEST)

    @action(methods=['get', 'patch'], detail=False, url_path='info')
    def user_info(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            serializer = self.get_serializer(instance=request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(self.get_serializer(request.user).data)


import json

from django.contrib.auth import login, logout
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from common.decorators import required_params
from common.mixins import LoginNotRequiredMixin
from users.forms import AuthenticationForm
from users.models import User
from users.serializers import DeviceSerializer, UserSerializer


class UserAPIView(LoginNotRequiredMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post'], detail=False)
    def registration(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
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
            request.data.update({'version': self.kwargs['version']})
            request.user.set_device(request.data)
            serializer = self.get_serializer(user)
            data = serializer.data
            return Response(data)
        else:
            errors = json.loads(form.errors.as_json())
            error_data = {e: [code.get('code')] for e, codes in errors.items() for code in codes}
            return Response(error_data, status=HTTP_400_BAD_REQUEST)

    @action(methods=['patch'], detail=False, url_path='info', permission_classes=[IsAuthenticated])
    def user_info(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response()

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def logout(self, request, *args, **kwargs):
        logout(request)
        return Response()

    @required_params
    @action(methods=['patch'], detail=False, permission_classes=[IsAuthenticated])
    def device(self, request, token, platform, *args, **kwargs):
        request.data.update({'version': self.kwargs['version']})
        device = request.user.set_device(request.data)
        serializer = DeviceSerializer(device)
        return Response(serializer.data)

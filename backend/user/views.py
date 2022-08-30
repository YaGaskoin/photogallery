from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions


class CreateUserView(CreateAPIView):

    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class GetUserView(APIView):

    model = User
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer



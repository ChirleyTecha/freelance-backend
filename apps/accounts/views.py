import logging
from rest_framework import status
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response


User = get_user_model()


class Register(APIView):
    """
    Register a new user
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        logging.info(
            f"User ID: {user.id}, endpoint: {request.path}, status: 201")

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class UserList(APIView):
    permission_classes = [IsAuthenticated]

    """
    List all users
    """

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

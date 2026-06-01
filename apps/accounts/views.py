import logging
from django.http import Http404
from rest_framework import status
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer, EmployerCreateSerializer, EmployerSerializer, WorkerSerializer, WorkerCreateSerializer
from rest_framework.response import Response
from .models import Employer, Worker


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


class MyProfile(APIView):
    """
    Fetch information of the loggedin user 
    """

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserDetail(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    """
    Retrieve, update or delete a user
    """

    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserList(APIView):
    permission_classes = [IsAuthenticated]

    """
    List all users
    """

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class EmployerList(APIView):
    permission_classes = [IsAdminUser]
    """
    List all employers
    """

    def get(self, request, format=None):
        employers = Employer.objects.select_related(
            "user").prefetch_related('client_documents')
        serializer = EmployerSerializer(employers, many=True)
        return Response(serializer.data)


class EmployerDetail(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    """
    Retrieve, update or delete a employer profile
    """

    def get_object(self, pk):
        try:
            employer = Employer.objects.get(pk=pk)
            return employer
        except Employer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        employer = self.get_object(pk)
        serializer = EmployerSerializer(employer)
        return Response(serializer.data)


class MyEmployer(APIView):
    """
    View employer details or create one
    """

    def post(self, request):
        # Prevent duplicates
        if hasattr(request.user, "employer"):
            return Response({"detail": "User already has a employer profile"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EmployerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save(user=request.user)

        logging.info(
            f"Employer ID: ${profile.id}, endpoint: me/employer/, status: ${status.HTTP_201_CREATED}")

        return Response(EmployerSerializer(profile).data, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        try:
            profile = request.user.employer
        except Employer.DoesNotExist:
            return Response({"detail": "No employer Profile"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployerSerializer(profile)
        return Response(serializer.data)


class WorkerList(APIView):
    permission_classes = [IsAuthenticated]

    """
    List all workers
    """

    def get(self, request, format=None):
        qs = Worker.objects.select_related("user").all()

        status_param = request.query_params.get("skills")

        if status_param:
            qs = qs.filter(skills=status_param)

        qs = qs.order_by("-id")

        serializer = WorkerSerializer(qs, many=True)

        return Response(serializer.data)


class WorkerDetail(APIView):
    """
    Rretrive or delete a worker profile
    """

    def get_object(self, pk):
        try:
            worker = Worker.objects.select_related("user").get(pk=pk)
            return worker
        except Worker.DoesNotExist:
            raise Http404

    def get(self, reques, pk, format=None):
        worker = self.get_object(pk)
        serializer = WorkerSerializer(worker)
        return Response(serializer.data)


class MyWorker(APIView):
    """
    Retrieve or create a worker profile
    """

    def post(self, request):
        # Prevent duplicates
        if hasattr(request.user, 'worker'):
            return Response({"detail": "User already has a worker profile"})

        serializer = WorkerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save(user=request.user)

        logging.info(
            f"Worker ID: ${profile.id}, endpoint: me/worker/, status: ${status.HTTP_201_CREATED}")

        return Response(WorkerSerializer(profile).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        try:
            profile = request.user.worker_profile
        except Worker.DoesNotExist:
            return Response({"detail": "No worker profile"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WorkerSerializer(profile)
        return Response(serializer.data)

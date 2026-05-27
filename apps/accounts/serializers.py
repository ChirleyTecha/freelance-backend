from django.contrib.auth import get_user_model
from rest_framework import serializers
from .utils.phone import normalize_mz_phone
from .models import Employer, Worker


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'phone', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def validate_phone_number(self, value):
        try:
            return normalize_mz_phone(value)  # return normalized value
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'name']


class EmployerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employer
        fields = ["address", "company_name"]


class EmployerSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source="user.name", read_only=True)

    class Meta:
        model = Employer
        fields = ['id', 'name', 'address', 'company_name']


class WorkerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = ["skills", "experience"]


class WorkerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name", read_only=True)

    class Meta:
        model = Worker
        fields = ['id', 'name', 'skills', 'experience']

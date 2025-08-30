from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    client = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = [
            "id",
            "project_name",
            "client",
            "users",
            "created_by",
            "created_at",
            "updated_at",
        ]


class ProjectCreateSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ["id", "project_name", "users"]

    def create(self, validated_data):
        users = validated_data.pop("users")
        project = Project.objects.create(**validated_data)
        project.users.set(users)
        return project


class ClientSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Client
        fields = [
            "id",
            "client_name",
            "projects",
            "created_at",
            "updated_at",
            "created_by",
        ]

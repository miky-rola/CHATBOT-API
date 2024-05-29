
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile, Conversation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email']

class ConversationSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'user_message', 'bot_response', 'timestamp']

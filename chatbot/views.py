from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile, Conversation
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ConversationSerializer
from .chatbot_logic import ChatbotLogic

# Initialize ChatbotLogic with a Hugging Face model
chatbot_logic = ChatbotLogic(model_name="gpt2")

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.data["username"], password=serializer.data["password"])
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": token.key
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat(request):
    username = request.data.get("username")
    email = request.data.get("email")
    user_message = request.data.get("message")

    if not username or not email or not user_message:
        return Response({"error": "Please provide username, email, and message."}, status=status.HTTP_400_BAD_REQUEST)

    user, created = UserProfile.objects.get_or_create(username=username, email=email)
    response = chatbot_logic.generate_response(user_message)

    conversation = Conversation.objects.create(user=user, user_message=user_message, bot_response=response)

    return Response({"response": response}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversation_history(request, username):
    try:
        user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    conversations = Conversation.objects.filter(user=user).order_by("timestamp")
    serializer = ConversationSerializer(conversations, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

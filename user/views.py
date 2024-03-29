from rest_framework import viewsets
from rest_framework import generics, permissions

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer, SubscriptionSerializer
from utils import auth
from django.contrib.auth import get_user_model

from .models import Subscription
from rest_framework.permissions import AllowAny
from .permissions import IsAdminUserOrSelf 
from rest_framework_simplejwt.authentication import JWTAuthentication



# Create your views here.
#

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = ()
  
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUserOrSelf,)


class AllUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class SubscriptionView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAdminUserOrSelf,)

    def perform_create(self, serializer):
        user = self.request.user
        
        serializer.save(user_id=user)

class UnsubscriptionView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)
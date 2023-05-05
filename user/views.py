from rest_framework import viewsets
from rest_framework import generics, permissions

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer
from utils import auth
from django.contrib.auth import get_user_model


from rest_framework.permissions import AllowAny
from .permissions import IsAdminUserOrSelf 



# Create your views here.
#

User = get_user_model()

# class UserViewSet(viewsets.ModelViewSet):

#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def retrieve(self, request, *args, **kwargs):
#         response = super(*args, **kwargs)
#         print('res: ', response)
#         return response


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    # def post(self, request):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user = serializer.save()
    #         if user:
    #             payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    #             token = api_settings.JWT_ENCODE_HANDLER(payload)
    #             return Response({'token': token}, status=201)
    #     return Response(serializer.errors, status=400)
  
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


# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         print(email)
#         print(password)
#         user = authenticate(request, email=email, password=password)
#         if user:
#             login(request, user)
#             payload = api_settings.JWT_PAYLOAD_HANDLER(user)
#             token = api_settings.JWT_ENCODE_HANDLER(payload)
#             return Response({'token': token}, status=200)
#         return Response({'error': 'Invalid credentials'}, status=401)


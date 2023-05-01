from .models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from utils import auth
# Create your views here.
#
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super(*args, **kwargs)
        print('res: ', response)
        return response


class RegisterView(APIView):

    def post(self, request):

        data = request.data
        register_serializer = RegisterSerializer(data=data)
        register_serializer.is_valid(raise_exception=True)

        user_serializer = UserSerializer(data=data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        data = user_serializer.data
        data['token'] = auth.get_jwt(data.get('pk'))

        return Response(data)




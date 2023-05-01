from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.token = 'this is token'
        return instance

class LoginSerializer(serializers.Serializer):
    pass

class RegisterSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)
    position = serializers.ChoiceField(choices=User.POSITION)

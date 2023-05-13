from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from .models import POSITION 

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username', 'position','school')
        read_only_fields = ('id',)



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        
        try:
        # 首先调用父类的 validate() 方法验证用户凭证
            data = super().validate(attrs)

            # 判断用户是否被禁用
            if not self.user.is_active:
                raise serializers.ValidationError('User is not active')

        
            # 获取用户信息
            user = self.user or self.username_field.get_user(self.validated_data[self.username_field])
            # 在返回的字典中添加用户数据
            data['id'] = user.id
            data['username'] = user.username
            data['email'] = user.email
            data['position'] = user.position
            data['school'] = user.school
            # ...

            return data

        except AuthenticationFailed:
            raise serializers.ValidationError('Email or password was wrong')


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    position = serializers.ChoiceField(required=True, choices=POSITION)


    token = serializers.SerializerMethodField('get_tokens')

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'position', 'token')
        extra_kwargs = {
            'username': {'required': True},
            'position': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            position=validated_data['position'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user
       


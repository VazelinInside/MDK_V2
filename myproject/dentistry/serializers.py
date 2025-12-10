from rest_framework import serializers
from .models import Role, Profession, User, Service, Diagnosis, Reception, Review
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['id'] = user.id
        token['email'] = user.email
        token['firstname'] = user.firstname
        token['lastname'] = user.lastname
        token['is_staff'] = user.is_staff
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'firstname': self.user.firstname,
            'lastname': self.user.lastname,
            'is_staff': self.user.is_staff
        }
        
        return data

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    patronymic = serializers.CharField(required=True, allow_blank=True)
    phone = serializers.CharField()
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        if 'patronymic' not in validated_data:
            validated_data['patronymic'] = ''
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Неверный email или пароль")
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'firstname', 'lastname', 'patronymic', 
                 'phone', 'role', 'profession', 'is_staff')
        read_only_fields = ('id', 'email')
        extra_kwargs = {
            'patronymic': {'required': False, 'allow_blank': True}
        }


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = [
            'id',
            'name',
        ]


class ProfessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profession
        fields = [
            'id',
            'name',
        ]


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'description',
            'price',
        ]


class DiagnosisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Diagnosis
        fields = [
            'id',
            'name',
            'code',
        ]


class ReceptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reception
        fields = [
            'id',
            'data_time',
            'service',
            'diagnosis',
            'users',
        ]


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            'id',
            'comment',
            'date',
            'reception',
        ]
from rest_framework import generics, status
from .models import Role, Profession, Service, Diagnosis, User, Reception, Review
from .serializers import (RoleSerializer, ProfessionSerializer, 
                         ServiceSerializer, DiagnosisSerializer,
                         UserSerializer, ReceptionSerializer,
                         ReviewSerializer, CustomTokenObtainPairSerializer)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate
from .permissions import IsAdminUser
from django.views.decorators.csrf import csrf_exempt


@swagger_auto_schema(method='post', request_body=RegisterSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = CustomTokenObtainPairSerializer.get_token(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'firstname': user.firstname,
                'lastname': user.lastname
            }
        }, status=status.HTTP_201_CREATED)

@swagger_auto_schema(method='post', request_body=LoginSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_view(request):
    data = request.data
    email = data.get('email', None)
    password = data.get('password', None)
    if email is None or password is None:
        return Response({'error': 'Нужен и логин, и пароль'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if user is None:
        return Response({'error': 'Неверные данные'}, status=status.HTTP_401_UNAUTHORIZED)
    refresh = CustomTokenObtainPairSerializer.get_token(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
            'id': user.id,
            'email': user.email,
            'firstname': user.firstname,
            'lastname': user.lastname
        }
    }, status=status.HTTP_200_OK)

@swagger_auto_schema(method='post')
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    refresh_token = request.data.get('refresh_token')
    if not refresh_token:
        return Response({'error': 'Необходим Refresh token'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception as e:
        return Response({'error': 'Неверный Refresh token'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'success': 'Выход успешен'}, status=status.HTTP_200_OK)


class RoleListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class ProfessionListCreateView(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class ProfessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class ServiceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class DiagnosisListCreateView(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer


class DiagnosisRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
    def get_object(self):
        if self.request.user.is_staff:
            return generics.get_object_or_404(User, pk=self.kwargs.get('pk'))
        return self.request.user
    
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReceptionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Reception.objects.all()
    serializer_class = ReceptionSerializer


class ReceptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Reception.objects.all()
    serializer_class = ReceptionSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('roles/', views.RoleListCreateView.as_view()),
    path('roles/<int:pk>/', views.RoleRetrieveUpdateDestroyView.as_view()),
    path('professions/', views.ProfessionListCreateView.as_view()),
    path('professions/<int:pk>/', views.ProfessionRetrieveUpdateDestroyView.as_view()),
    path('services/', views.ServiceListCreateView.as_view()),
    path('services/<int:pk>/', views.ServiceRetrieveUpdateDestroyView.as_view()),
    path('diagnosis/', views.DiagnosisListCreateView.as_view()),
    path('diagnosis/<int:pk>/', views.DiagnosisRetrieveUpdateDestroyView.as_view()),
    path('users/', views.UserListView.as_view()),
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroyView.as_view()),
    path('receptions/', views.ReceptionListCreateView.as_view()),
    path('receptions/<int:pk>/', views.ReceptionRetrieveUpdateDestroyView.as_view()),
    path('reviews/', views.ReviewListCreateView.as_view()),
    path('reviews/<int:pk>/', views.ReviewRetrieveUpdateDestroyView.as_view()),
    path('register/', views.register_view),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, UserDetailView, AllUserView, SubscriptionView, UnsubscriptionView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', AllUserView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),

    path('users/subscription/', SubscriptionView.as_view(), name='subscription'),
    path('users/unsubscription/<int:pk>', UnsubscriptionView.as_view(), name='unsubscription')
]

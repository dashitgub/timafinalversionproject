from django.urls import path
from .views import test_detail, test_list, UserRegisterView, UserLoginView, test_result
from . import views

urlpatterns = [
    path("", test_list, name="test_list"),
    path("<int:test_id>/", test_detail, name="test_detail"),
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('result/<str:username>/', views.test_result, name='test_result'),
    path('login/', UserLoginView.as_view(), name='user_login'),
]

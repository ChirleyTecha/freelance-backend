from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("auth/register/", views.Register.as_view()),
    path("users/", views.UserList.as_view()),
]

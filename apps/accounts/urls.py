from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("auth/register/", views.Register.as_view()),
    path("users/", views.UserList.as_view()),
    path("workers/", views.WorkerList.as_view()),
    path("employers/", views.EmployerList.as_view()),
    path("me/employer/", views.MyEmployer.as_view()),
    path("me/worker/", views.MyWorker.as_view()),
]

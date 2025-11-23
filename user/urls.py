"""
This module contains all the end points related to user.
"""

from django.urls import path
from .views import(
    UserRegisterAPIView
)

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register-user"),

]

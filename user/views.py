"""
This module contains views for User related operations.
User register, User login, user logout, user profile management and user search functionality
"""

from rest_framework.views import APIView
from rest_framework.request import Request

from core.utils.responses import (
    response_success,
    response_bad_request,
    response_created,
    response_forbidden,
    response_unauthorized,
)

from .models import User
from .serializers import UserSerializer

class UserRegisterAPIView(APIView):
    """
    APIView to register a user
    """

    def post(self, request: Request):
        """
        Handle Post request to register a new user.
        """
        try:
            print(request.data)
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get("email")
                print("After Validation", email)
                if User.objects.filter(email=email).exists():
                    return response_bad_request(
                        errors="Worng Email.",
                        message="Email already used by someone."
                    )
                user = serializer.save()
                return response_created(
                    data=user,
                    message="User registered successfully."
                )
            print("ERROR in DATA validation", str(e))
            return response_bad_request(
                errors=serializer.errors,
                message="Invalid data provided."
            )
        except Exception as e:
            print("ERROR", str(e))
            return response_bad_request(
                errors=str(e),
                message="An Error Occured."
            )

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import RetailerRegistrationSerializer
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .models import Retailer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

User = get_user_model()


class RetailerRegisterView(generics.CreateAPIView):
    queryset = Retailer.objects.all()
    serializer_class = RetailerRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Retailer registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetailerLoginView(APIView):
    permission_classes = [AllowAny]  # No authentication required for login

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                retailer = Retailer.objects.get(user=user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "token": token.key,
                    "retailer_id": retailer.pk,
                    "business_name": retailer.business_name
                }, status=status.HTTP_200_OK)
            except Retailer.DoesNotExist:
                return Response({"error": "User is not a retailer"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class RetailerLogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication

    def post(self, request):
        try:
            # Delete the user's token to log them out
            Token.objects.filter(user=request.user).delete()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
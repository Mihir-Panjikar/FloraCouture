from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import generics, status
from .serializers import RetailerSerializer
from .models import Retailer
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView


class RegisterRetailer(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RetailerSerializer(data=request.data)
        if serializer.is_valid():
            retailer = serializer.save()
            token, _ = Token.objects.get_or_create(
                user=retailer)  # Retailer is the user model
            return Response(
                {"message": "Retailer registered successfully", "token": token.key},
                status=201
            )
        return Response(serializer.errors, status=400)


class LoginRetailer(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        retailer = authenticate(username=username, password=password)

        if retailer:
            token, _ = Token.objects.get_or_create(
                user=retailer)  # Retailer is the user model
            return Response({"message": "Login successful", "token": token.key}, status=200)
        return Response({"error": "Invalid credentials"}, status=400)


class RetailerRegisterView(generics.CreateAPIView):
    queryset = Retailer.objects.all()
    serializer_class = RetailerSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            retailer = serializer.save()
            token, _ = Token.objects.get_or_create(user=retailer)
            return Response({
                "message": "Retailer registered successfully",
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetailerProfileView(RetrieveAPIView):
    queryset = Retailer.objects.all()
    serializer_class = RetailerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user  # Return the logged-in retailer


class RetailerProfileUpdateView(UpdateAPIView):
    queryset = Retailer.objects.all()
    serializer_class = RetailerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user  # Return the logged-in retailer


class LogoutRetailer(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()  # Remove the token
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid request or already logged out"}, status=status.HTTP_400_BAD_REQUEST)

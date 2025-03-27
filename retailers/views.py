from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from .serializers import RetailerSerializer
from django.contrib.auth.hashers import check_password, make_password
from .models import Retailer


# 1️⃣ Retailer Registration API
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


# 2️⃣ Retailer Login API
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


# 3️⃣ Retailer Profile API (Retrieve)
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


# 4️⃣ Retailer Profile Update API
class RetailerProfileUpdateView(UpdateAPIView):
    queryset = Retailer.objects.all()
    serializer_class = RetailerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user  # Return the logged-in retailer


# 5️⃣ Retailer Logout API
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


# 6️⃣ Change Password API
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response({"error": "Both old and new passwords are required"}, status=400)

        if not check_password(old_password, request.user.password):
            return Response({"error": "Incorrect old password"}, status=400)

        request.user.password = make_password(new_password)
        request.user.save()

        return Response({"message": "Password changed successfully"}, status=200)


# 7️⃣ Retailer List API (Admin Only)
class RetailerListView(ListAPIView):
    queryset = Retailer.objects.all()
    serializer_class = RetailerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


# 8️⃣ Retailer Delete Account API
class DeleteRetailerView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "Retailer account deleted successfully"}, status=200)


# 9️⃣ Forgot Password API (Reset Token-Based)
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        try:
            retailer = Retailer.objects.get(email=email)
        except Retailer.DoesNotExist:
            return Response({"error": "Email not registered"}, status=400)

        # For demonstration, we're returning a dummy reset link
        reset_link = f"http://example.com/reset-password/{retailer.pk}/"
        return Response({"message": "Password reset link sent", "reset_link": reset_link}, status=200)
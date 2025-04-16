from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json

from .serializers import CustomerRegistrationSerializer, RetailerRegistrationSerializer
from retailers.models import Retailer
from customers.models import Customer

User = get_user_model()

# Customer registration view
class CustomerRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = CustomerRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            customer = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(customer)
            
            return Response({
                'user_id': customer.pk,
                'username': customer.username,
                'email': customer.email,
                'token': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retailer registration view
class RetailerRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RetailerRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            retailer = serializer.save()
            
            # For retailers, we don't immediately provide a token since they need verification
            return Response({
                'user_id': retailer.pk,
                'username': retailer.username,
                'email': retailer.email,
                'message': 'Registration successful. Your account is pending approval.'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login view (handles both customer and retailer login)
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user_type = request.data.get('user_type', 'customer')  # Default to customer
        
        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response({'error': 'Invalid credentials'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        # Check user type and permissions
        if user_type == 'customer' and isinstance(user, Customer):
            # Generate JWT tokens for customer
            refresh = RefreshToken.for_user(user)
            return Response({
                'user_id': user.pk,
                'username': user.username,
                'email': user.email,
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'user_type': 'customer'
            })
        elif user_type == 'retailer' and isinstance(user, Retailer):
            # Check if retailer is verified
            if not user.is_verified:
                return Response({'error': 'Your account is pending approval'}, 
                              status=status.HTTP_401_UNAUTHORIZED)
                
            # Generate JWT tokens for verified retailer
            refresh = RefreshToken.for_user(user)
            return Response({
                'user_id': user.pk,
                'username': user.username,
                'email': user.email,
                'store_name': user.store_name,
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'user_type': 'retailer'
            })
        else:
            return Response({'error': 'Invalid account type'}, 
                          status=status.HTTP_401_UNAUTHORIZED)

class RetailerLogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication

    def post(self, request):
        try:
            # Delete the user's token to log them out
            Token.objects.filter(user=request.user).delete()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_protect
def contact_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        
        # Process the contact form data - e.g., send email, save to database
        # You could use Django's send_mail function or create a Contact model
        
        return JsonResponse({'status': 'success', 'message': 'Your message has been received'})
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


from django.shortcuts import render

def auth_page(request):
    return render(request, 'frontend/auth.html')
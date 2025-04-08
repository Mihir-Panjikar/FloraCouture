from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from retailers.models import Retailer
from rest_framework.authtoken.models import Token

User = get_user_model()


class RetailerAPITestCase(TestCase):
    def setUp(self):
        """Set up test data and client."""
        self.client = APIClient()
        self.register_url = reverse('retailer-register')
        self.login_url = reverse('retailer-login')
        self.logout_url = reverse('retailer-logout')

        # Create a test user and retailer for login/logout tests
        self.test_user = User.objects.create_user(
            username='testretailer',
            password='testpassword123',
            email='test@example.com'
        )

        self.test_retailer = Retailer.objects.create(
            user=self.test_user,
            business_name='Test Flower Shop',
            phone_number='1234567890',
            address='123 Test St'
        )

        # Create token for authentication tests
        self.token = Token.objects.create(user=self.test_user)

    def tearDown(self):
        """Clean up after tests."""
        User.objects.all().delete()
        Retailer.objects.all().delete()
        Token.objects.all().delete()

    # Registration Tests
    def test_retailer_registration_success(self):
        """Test successful retailer registration."""
        data = {
            'username': 'newretailer',
            'password': 'securepassword123',
            'email': 'new@example.com',
            'business_name': 'New Flower Shop',
            'phone_number': '9876543210',
            'address': '456 New St'
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],
                         'Retailer registered successfully')
        self.assertTrue(User.objects.filter(username='newretailer').exists())
        self.assertTrue(Retailer.objects.filter(
            business_name='New Flower Shop').exists())

    def test_retailer_registration_duplicate_username(self):
        """Test registration with duplicate username."""
        data = {
            'username': 'testretailer',  # Already exists
            'password': 'securepassword123',
            'email': 'another@example.com',
            'business_name': 'Another Flower Shop',
            'phone_number': '5555555555',
            'address': '789 Another St'
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retailer_registration_invalid_data(self):
        """Test registration with missing required fields."""
        data = {
            'username': 'incompleteretailer',
            'password': 'password123'
            # Missing required fields
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Login Tests
    def test_retailer_login_success(self):
        """Test successful retailer login."""
        data = {
            'username': 'testretailer',
            'password': 'testpassword123'
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('retailer_id', response.data)
        self.assertEqual(response.data['business_name'], 'Test Flower Shop')

    def test_retailer_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        data = {
            'username': 'testretailer',
            'password': 'wrongpassword'
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    def test_retailer_login_nonexistent_user(self):
        """Test login with non-existent user."""
        data = {
            'username': 'nonexistentuser',
            'password': 'password123'
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    # Logout Tests
    def test_retailer_logout_success(self):
        """Test successful retailer logout."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Successfully logged out')

        # Verify token has been deleted
        self.assertFalse(Token.objects.filter(user=self.test_user).exists())

    def test_retailer_logout_unauthorized(self):
        """Test logout without authentication."""
        # No authentication provided
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retailer_logout_invalid_token(self):
        """Test logout with invalid token."""
        self.client.credentials(HTTP_AUTHORIZATION='Token invalidtokenstring')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

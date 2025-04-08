from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Retailer
from rest_framework.authtoken.models import Token


class RetailerAPITests(TestCase):
    """Test suite for Retailer API endpoints"""

    def setUp(self):
        """Set up test data for all tests."""
        self.client = APIClient()

        # API URLs
        self.register_url = reverse('retailer-register')
        self.login_url = reverse('login')
        self.profile_url = reverse('retailer-profile')
        self.profile_update_url = reverse('retailer-profile-update')
        self.logout_url = reverse('retailer-logout')
        self.change_password_url = reverse('change_password')
        self.retailers_list_url = reverse('retailers_list')
        self.delete_account_url = reverse('delete_account')
        self.forgot_password_url = reverse('forgot_password')

        # Create test retailer
        self.test_retailer = Retailer.objects.create_user(
            username='testretailer',
            email='test@example.com',
            password='testpassword123',
            store_name='Test Flower Shop',
            business_name='Test Floral Business',
            phone_number='1234567890',
            address='123 Test St, Test City'
        )

        # Create token for authentication tests
        self.token = Token.objects.create(user=self.test_retailer)

        # Create admin user for admin-only endpoints
        self.admin_user = Retailer.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword123'
        )
        self.admin_token = Token.objects.create(user=self.admin_user)

    def tearDown(self):
        """Clean up after tests."""
        Token.objects.all().delete()
        Retailer.objects.all().delete()

    # Registration Tests
    def test_retailer_registration_success(self):
        """Test successful retailer registration."""
        data = {
            'username': 'newretailer',
            'email': 'new@example.com',
            'password': 'securepassword123',
            'store_name': 'New Flower Shop',
            'business_name': 'New Floral Business',
            'phone_number': '9876543210',
            'address': '456 New St, New City'
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'],
                         'Retailer registered successfully')

        # Verify retailer was created
        self.assertTrue(Retailer.objects.filter(
            username='newretailer').exists())

    def test_retailer_registration_duplicate_username(self):
        """Test registration with duplicate username."""
        data = {
            'username': 'testretailer',  # Already exists
            'email': 'another@example.com',
            'password': 'securepassword123',
            'store_name': 'Another Flower Shop'
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retailer_registration_invalid_data(self):
        """Test registration with missing required fields."""
        data = {
            'username': 'incompleteretailer',
            # Missing email and other required fields
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
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Login successful')

    def test_retailer_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        data = {
            'username': 'testretailer',
            'password': 'wrongpassword'
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    # Profile Tests
    def test_get_retailer_profile(self):
        """Test retrieving retailer profile."""
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testretailer')
        self.assertEqual(response.data['store_name'], 'Test Flower Shop')

    def test_get_profile_unauthenticated(self):
        """Test retrieving profile without authentication."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_retailer_profile(self):
        """Test updating retailer profile."""
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        update_data = {
            'store_name': 'Updated Flower Shop',
            'address': 'Updated Address'
        }

        response = self.client.patch(
            self.profile_update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the profile was updated
        self.test_retailer.refresh_from_db()
        self.assertEqual(self.test_retailer.store_name, 'Updated Flower Shop')
        self.assertEqual(self.test_retailer.address, 'Updated Address')

    def test_update_profile_unauthenticated(self):
        """Test updating profile without authentication."""
        update_data = {
            'store_name': 'Unauthorized Update'
        }

        response = self.client.patch(
            self.profile_update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Logout Tests
    def test_retailer_logout_success(self):
        """Test successful retailer logout."""
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Logout successful')

        # Verify token was deleted
        self.assertFalse(Token.objects.filter(
            user=self.test_retailer).exists())

    def test_retailer_logout_unauthenticated(self):
        """Test logout without authentication."""
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Change Password Tests
    def test_change_password_success(self):
        """Test successful password change."""
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        data = {
            'old_password': 'testpassword123',
            'new_password': 'newpassword456'
        }

        response = self.client.post(
            self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try logging in with new password
        self.client.credentials()  # Clear credentials
        login_data = {
            'username': 'testretailer',
            'password': 'newpassword456'
        }
        login_response = self.client.post(
            self.login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_change_password_incorrect_old_password(self):
        """Test password change with incorrect old password."""
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword456'
        }

        response = self.client.post(
            self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Delete Account Tests
    def test_delete_account_success(self):
        """Test successful account deletion."""
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.delete(self.delete_account_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'],
                         'Retailer account deleted successfully')

        # Verify account was deleted
        self.assertFalse(Retailer.objects.filter(
            username='testretailer').exists())

    def test_delete_account_unauthenticated(self):
        """Test account deletion without authentication."""
        response = self.client.delete(self.delete_account_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Forgot Password Tests
    def test_forgot_password_success(self):
        """Test successful password reset request."""
        data = {
            'email': 'test@example.com'
        }

        response = self.client.post(
            self.forgot_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Password reset link sent')
        self.assertIn('reset_link', response.data)

    def test_forgot_password_invalid_email(self):
        """Test password reset request with unregistered email."""
        data = {
            'email': 'nonexistent@example.com'
        }

        response = self.client.post(
            self.forgot_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Email not registered')

    # Retailers List Tests (Admin Only)
    def test_list_retailers_admin(self):
        """Test listing all retailers as admin."""
        # Authenticate as admin
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')

        response = self.client.get(self.retailers_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # At least admin and test retailer
        self.assertGreaterEqual(len(response.data), 2)

    def test_list_retailers_non_admin(self):
        """Test listing retailers as non-admin user."""
        # Authenticate as regular retailer
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(self.retailers_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

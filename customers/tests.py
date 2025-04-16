from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Customer


class CustomerAPITests(APITestCase):
    """Test suite for Customer API endpoints"""

    def setUp(self):
        """Set up for the tests."""
        # Since APITestCase already provides a client, we don't need to set it
        # self.client = APIClient()  # Remove this line
        # Added the missing register_url
        self.register_url = reverse('customer-register')
        self.login_url = reverse('customer-login')
        self.profile_url = reverse('customer-profile')

        # Test user data
        self.user_data = {
            'username': 'testcustomer',
            'email': 'test@example.com',
            'password': 'securepassword123',
            'phone_number': '1234567890',
            'address': '123 Test St, Test City'
        }

        # Create a test user for authentication tests
        self.test_user = Customer.objects.create_user(
            username='existingcustomer',
            email='existing@example.com',
            password='existingpassword123',
            phone_number='9876543210',
            address='456 Existing Ave'
        )

    # Registration Tests
    def test_customer_registration_success(self):
        """Test successful customer registration."""
        response = self.client.post(
            self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertTrue(Customer.objects.filter(
            username='testcustomer').exists())

    def test_customer_registration_duplicate_email(self):
        """Test registration with duplicate email."""
        # First registration
        self.client.post(self.register_url, self.user_data, format='json')

        # Second registration with same email
        duplicate_data = self.user_data.copy()
        duplicate_data['username'] = 'anothercustomer'
        response = self.client.post(
            self.register_url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_registration_invalid_data(self):
        """Test registration with missing required fields."""
        invalid_data = {
            'username': 'incompletecustomer',
            'password': 'password123'
            # Missing email and other fields
        }
        response = self.client.post(
            self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Login Tests
    def test_customer_login_success(self):
        """Test successful customer login."""
        login_data = {
            'username': 'existingcustomer',
            'password': 'existingpassword123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_customer_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        login_data = {
            'username': 'existingcustomer',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_login_nonexistent_user(self):
        """Test login with non-existent user."""
        login_data = {
            'username': 'nonexistentuser',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Profile Tests
    def test_get_customer_profile(self):
        """Test retrieving customer profile."""
        # Authenticate
        self.client.force_authenticate(user=self.test_user)

        # Get profile
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existingcustomer')
        self.assertEqual(response.data['email'], 'existing@example.com')
        self.assertEqual(response.data['phone_number'], '9876543210')
        self.assertEqual(response.data['address'], '456 Existing Ave')

    def test_update_customer_profile(self):
        """Test updating customer profile."""
        # Authenticate
        self.client.force_authenticate(user=self.test_user)

        # Update data
        update_data = {
            'phone_number': '5555555555',
            'address': 'Updated Address'
        }

        # Update profile
        response = self.client.patch(
            self.profile_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], '5555555555')
        self.assertEqual(response.data['address'], 'Updated Address')

        # Verify database was updated
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.phone_number, '5555555555')
        self.assertEqual(self.test_user.address, 'Updated Address')

    def test_profile_unauthorized_access(self):
        """Test unauthorized access to profile endpoint."""
        # No authentication
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Additional Tests
    def test_customer_password_change(self):
        """Test customer password change."""
        # Authenticate
        self.client.force_authenticate(user=self.test_user)

        password_change_url = reverse('customer-password-change')
        password_data = {
            'old_password': 'existingpassword123',
            'new_password': 'newpassword456'
        }

        response = self.client.post(
            password_change_url, password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the password was changed by trying to login
        self.client.logout()
        login_data = {
            'username': 'existingcustomer',
            'password': 'newpassword456'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

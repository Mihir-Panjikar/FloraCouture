from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Product
from decimal import Decimal
from rest_framework.authtoken.models import Token
import tempfile
from PIL import Image
from typing import Any
from rest_framework.response import Response

User = get_user_model()


class ProductAPITests(TestCase):
    """Test suite for Product API endpoints"""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()

        # Create test users (retailers)
        self.retailer1 = User.objects.create_user(
            username='retailer1',
            email='retailer1@example.com',
            password='password123'
        )

        self.retailer2 = User.objects.create_user(
            username='retailer2',
            email='retailer2@example.com',
            password='password123'
        )

        # Create tokens for authentication
        self.retailer1_token = Token.objects.create(user=self.retailer1)
        self.retailer2_token = Token.objects.create(user=self.retailer2)

        # Create test products
        self.product1 = Product.objects.create(
            retailer=self.retailer1,
            name='Rose Bouquet',
            description='Beautiful red roses',
            price=Decimal('49.99'),
            stock=100
        )

        self.product2 = Product.objects.create(
            retailer=self.retailer2,
            name='Tulip Arrangement',
            description='Colorful tulips',
            price=Decimal('39.99'),
            stock=50
        )

        # Create temp image for testing file uploads
        # Set up API URLs
        self.create_product_url = reverse('create_product')
        self.list_products_url = reverse('list_products')
        self.retrieve_product_url = reverse(
            'retrieve_product', args=[self.product1.pk])
        self.update_product_url = reverse(
            'update_product', args=[self.product1.pk])
        self.delete_product_url = reverse(
            'delete_product', args=[self.product1.pk])

    def get_temporary_image(self):
        """Create a temporary image for testing."""
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        return tmp_file

    def tearDown(self):
        """Clean up after tests."""
        # Close the temp image file
        if hasattr(self, 'image'):
            self.image.close()

    # Create Product Tests
        # Using setattr instead of credentials method for type checking
    def test_create_product(self):
        """Test product creation with authentication."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.retailer1_token.key}')

        data = {
            'name': 'Lily Bouquet',
            'description': 'Fresh lilies arrangement',
            'price': '59.99',
            'stock': 80
        }
        
        response = self.client.post(
            self.create_product_url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Lily Bouquet')
        self.assertEqual(response.data['retailer'], self.retailer1.pk)

        # Verify product was created in database
        self.assertTrue(Product.objects.filter(name='Lily Bouquet').exists())
        """Test product creation without authentication."""
        data = {
            'name': 'Daisy Arrangement',
            'description': 'Beautiful daisies',
            'price': '29.99',
            'stock': 20
        }

        response = self.client.post(
            self.create_product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_invalid_data(self):
        """Test product creation with invalid data."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.retailer1_token.key}')

        # Missing required fields
        response_data = response.data if hasattr(response, 'data') else {}  # type: ignore
        self.assertIn('name', response_data)
        self.assertIn('price', response_data)
    def test_create_product_invalid_data(self):
        """Test product creation with invalid data."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.retailer1_token.key}')

        # Missing required fields
        data = {}

        response = self.client.post(
            self.create_product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('price', response.data)

    # Retrieve Product Tests
    def test_retrieve_product(self):
        """Test retrieving a single product."""
        response = self.client.get(self.retrieve_product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_list_products(self):
        """Test listing all products."""
        response = self.client.get(self.list_products_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Update Product Tests
    def test_update_product_success(self):
        """Test successful product update by owner."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.retailer1_token.key}')
        response_data = response.data if hasattr(response, 'data') else {}  # type: ignore
        self.assertEqual(response_data.get('name'), 'Updated Rose Bouquet')
        self.assertEqual(response_data.get('price'), '54.99')
            'name': 'Updated Rose Bouquet',
        updated_product = Product.objects.get(pk=self.product1.pk)
            'stock': 75
        }

        response = self.client.patch(
            self.update_product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_update_product_success(self):
        """Test successful product update by owner."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.retailer1_token.key}')
        
        data = {
            'name': 'Updated Rose Bouquet',
            'price': '54.99',
            'stock': 75
        }

        response = self.client.patch(
            self.update_product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Rose Bouquet')
        self.assertEqual(response.data['price'], '54.99')

        # Verify database was updated
        updated_product = Product.objects.get(pk=self.product1.pk)
        self.assertEqual(updated_product.name, 'Updated Rose Bouquet')
        self.assertEqual(updated_product.price, Decimal('54.99'))
        # Verify product was not changed
        unchanged_product = Product.objects.get(id=self.product1.id)
        self.assertEqual(unchanged_product.name, 'Rose Bouquet')

    def test_update_product_unauthenticated(self):
        """Test update product without authentication."""
        data = {
            'name': 'Unauthorized Update',
            'price': '99.99'
        }

        response = self.client.patch(
            self.update_product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Product.objects.filter(pk=self.product1.pk).exists())
    # Delete Product Tests
    def test_delete_product_success(self):
        """Test successful product deletion by owner."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.retailer1_token.key}')
    def test_update_product_unauthenticated(self):
        """Test update product without authentication."""
        data = {
            'name': 'Unauthorized Update',
            'price': '99.99'
        }

        response = self.client.patch(
            self.update_product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Verify product still exists and wasn't changed
        self.assertTrue(Product.objects.filter(pk=self.product1.pk).exists())
    def test_delete_product_success(self):
        """Test successful product deletion by owner."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.retailer1_token.key}')

        response = self.client.delete(self.delete_product_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify product was deleted
        self.assertFalse(Product.objects.filter(pk=self.product1.pk).exists())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Verify product was not deleted
        self.assertTrue(Product.objects.filter(pk=self.product1.pk).exists())

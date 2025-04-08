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
        self.image = self.get_temporary_image()

        # Set up API URLs
        self.create_product_url = reverse('create_product')
        self.list_products_url = reverse('list_products')
        self.retrieve_product_url = reverse(
            'retrieve_product', args=[self.product1.id])
        self.update_product_url = reverse(
            'update_product', args=[self.product1.id])
        self.delete_product_url = reverse(
            'delete_product', args=[self.product1.id])

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
    def test_create_product_success(self):
        """Test successful product creation."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.retailer1_token.key}')

        data = {
            'name': 'Lily Bouquet',
            'description': 'Fresh lilies arrangement',
            'price': '59.99',
            'stock': 25,
            'image': self.image
        }

        response = self.client.post(
            self.create_product_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Lily Bouquet')
        self.assertEqual(response.data['retailer'], self.retailer1.id)

        # Verify product was created in database
        self.assertTrue(Product.objects.filter(name='Lily Bouquet').exists())

    def test_create_product_unauthenticated(self):
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
        data = {
            'description': 'Incomplete product data'
        }

        response = self.client.post(
            self.create_product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('price', response.data)

    # List Products Tests
    def test_list_products(self):
        """Test listing all products."""
        response = self.client.get(self.list_products_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Two products created in setUp
        self.assertEqual(len(response.data), 2)

    # Retrieve Product Tests
    def test_retrieve_product(self):
        """Test retrieving a single product."""
        response = self.client.get(self.retrieve_product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Rose Bouquet')
        self.assertEqual(response.data['price'], '49.99')

    def test_retrieve_nonexistent_product(self):
        """Test retrieving a nonexistent product."""
        nonexistent_url = reverse('retrieve_product', args=[
                                  999])  # ID that doesn't exist
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Update Product Tests
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
        updated_product = Product.objects.get(id=self.product1.id)
        self.assertEqual(updated_product.name, 'Updated Rose Bouquet')
        self.assertEqual(updated_product.price, Decimal('54.99'))

    def test_update_product_different_retailer(self):
        """Test update product by a different retailer (should fail)."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.retailer2_token.key}')

        data = {
            'name': 'Unauthorized Update',
            'price': '99.99'
        }

        response = self.client.patch(
            self.update_product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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

    # Delete Product Tests
    def test_delete_product_success(self):
        """Test successful product deletion by owner."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.retailer1_token.key}')

        response = self.client.delete(self.delete_product_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify product was deleted
        self.assertFalse(Product.objects.filter(id=self.product1.id).exists())

    def test_delete_product_different_retailer(self):
        """Test delete product by a different retailer (should fail)."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.retailer2_token.key}')

        response = self.client.delete(self.delete_product_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify product was not deleted
        self.assertTrue(Product.objects.filter(id=self.product1.id).exists())

    def test_delete_product_unauthenticated(self):
        """Test delete product without authentication."""
        response = self.client.delete(self.delete_product_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

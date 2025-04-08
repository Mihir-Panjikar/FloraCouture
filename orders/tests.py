from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Order, OrderItem
from products.models import Product
from rest_framework.authtoken.models import Token

User = get_user_model()


class OrderAPITests(TestCase):
    """Test suite for Order API endpoints"""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()

        # Create test users (customer and retailer)
        self.customer = User.objects.create_user(
            username='testcustomer',
            email='customer@example.com',
            password='customerpassword123'
        )

        self.retailer = User.objects.create_user(
            username='testretailer',
            email='retailer@example.com',
            password='retailerpassword123'
        )

        # Create tokens for authentication
        self.customer_token = Token.objects.create(user=self.customer)
        self.retailer_token = Token.objects.create(user=self.retailer)

        # Create test products
        self.product1 = Product.objects.create(
            name='Rose Bouquet',
            description='Beautiful red roses',
            price=49.99,
            stock=100
        )

        self.product2 = Product.objects.create(
            name='Tulip Arrangement',
            description='Colorful tulips',
            price=39.99,
            stock=50
        )

        # Create test orders
        self.customer_order = Order.objects.create(
            user=self.customer,
            status='Pending'
        )

        self.processed_order = Order.objects.create(
            user=self.customer,
            status='Processing'
        )

        # Create order items
        OrderItem.objects.create(
            order=self.customer_order,
            product=self.product1,
            quantity=2
        )

        OrderItem.objects.create(
            order=self.processed_order,
            product=self.product2,
            quantity=1
        )

        # Set up API URLs
        self.create_order_url = reverse('create-order')
        self.retrieve_order_url = reverse(
            'retrieve-order', args=[self.customer_order.id])
        self.update_order_status_url = reverse(
            'update-order-status', args=[self.customer_order.id])
        self.list_orders_url = reverse('list-orders')
        self.cancel_order_url = reverse(
            'cancel-order', args=[self.customer_order.id])
        self.cancel_processed_order_url = reverse(
            'cancel-order', args=[self.processed_order.id])

    # Create Order Tests
    def test_create_order_success(self):
        """Test successful order creation."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')

        data = {
            'status': 'Pending',
            'items': [
                {
                    'product': self.product1.id,
                    'quantity': 3
                }
            ]
        }

        response = self.client.post(self.create_order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 3)  # 2 existing + 1 new

    def test_create_order_unauthenticated(self):
        """Test order creation with no authentication."""
        data = {
            'status': 'Pending',
            'items': [
                {
                    'product': self.product1.id,
                    'quantity': 1
                }
            ]
        }

        response = self.client.post(self.create_order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Retrieve Order Tests
    def test_retrieve_order_success(self):
        """Test successful order retrieval."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')

        response = self.client.get(self.retrieve_order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.customer_order.id)

    def test_retrieve_order_unauthorized(self):
        """Test unauthorized order retrieval."""
        # No authentication
        response = self.client.get(self.retrieve_order_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Update Order Status Tests
    def test_update_order_status_success(self):
        """Test successful order status update."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')

        data = {
            'status': 'Processing'
        }

        response = self.client.patch(
            self.update_order_status_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         'Order status updated successfully')

        # Verify the order status was updated
        updated_order = Order.objects.get(id=self.customer_order.id)
        self.assertEqual(updated_order.status, 'Processing')

    def test_update_order_status_missing_status(self):
        """Test order status update with missing status field."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')

        data = {}  # Missing status field

        response = self.client.patch(
            self.update_order_status_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Status field is required')

    # List Orders Tests
    def test_list_customer_orders(self):
        """Test listing orders for a customer."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')

        response = self.client.get(self.list_orders_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Customer has 2 orders

    def test_list_orders_unauthenticated(self):
        """Test listing orders without authentication."""
        response = self.client.get(self.list_orders_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Cancel Order Tests
    def test_cancel_pending_order(self):
        """Test cancelling a pending order."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')

        response = self.client.delete(self.cancel_order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         'Order cancelled successfully')

        # Verify the order was deleted
        self.assertFalse(Order.objects.filter(
            id=self.customer_order.id).exists())

    def test_cancel_non_pending_order(self):
        """Test attempting to cancel a non-pending order."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')

        response = self.client.delete(self.cancel_processed_order_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error'], 'Cannot cancel an order that is not pending')

        # Verify the order was not deleted
        self.assertTrue(Order.objects.filter(
            id=self.processed_order.id).exists())

    def test_cancel_order_unauthenticated(self):
        """Test cancelling an order without authentication."""
        response = self.client.delete(self.cancel_order_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

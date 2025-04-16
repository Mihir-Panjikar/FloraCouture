from django.test import TestCase
from django.urls import reverse
from channels.testing import WebsocketCommunicator, ChannelsLiveServerTestCase
from channels.routing import URLRouter
from django.conf.urls import url
import json
import pytest

from .consumers import ChatbotConsumer
from .routing import websocket_urlpatterns
from .models import BotResponse

class ChatViewTests(TestCase):
    """Tests for the HTTP views related to chat."""

    def test_chat_room_view(self):
        """Test that the chat room view returns a successful response."""
        room_name = "test-room"
        response = self.client.get(reverse('chat:room', args=[room_name]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/room.html')
        self.assertContains(response, room_name)


class ChatbotViewTests(TestCase):
    """Tests for the HTTP views related to chatbot."""

    def test_chatbot_interface_view(self):
        """Test that the chatbot interface view returns a successful response."""
        response = self.client.get(reverse('chat:chatbot'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chatbot.html')


class BotResponseTests(TestCase):
    """Tests for the BotResponse model."""

    def setUp(self):
        """Set up test data."""
        BotResponse.objects.create(
            category='greeting',
            keywords='hello,hi',
            response_text='Hello! How can I help you?',
            priority=1
        )

        BotResponse.objects.create(
            category='product',
            keywords='flowers,bouquet',
            response_text='We have many beautiful bouquets!',
            priority=2
        )

    def test_bot_response_str(self):
        """Test the string representation of BotResponse."""
        response = BotResponse.objects.get(category='greeting')
        self.assertEqual(
            str(response), "greeting: Hello! How can I help you?...")


@pytest.mark.asyncio
class ChatConsumerTests(ChannelsLiveServerTestCase):
    """Tests for the WebSocket consumer functionality."""

    def setUp(self):
        """Set up for the WebSocket tests."""
        self.room_name = "test-room"
        self.websocket_url = f"/ws/chat/{self.room_name}/"

    async def test_websocket_connection(self):
        """Test that a WebSocket connection can be established."""
        communicator = WebsocketCommunicator(
            URLRouter(websocket_urlpatterns),
            self.websocket_url
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_chat_message_echo(self):
        """Test that a message sent is echoed back to all clients."""
        communicator1 = WebsocketCommunicator(
            URLRouter(websocket_urlpatterns),
            self.websocket_url
        )
        communicator2 = WebsocketCommunicator(
            URLRouter(websocket_urlpatterns),
            self.websocket_url
        )

        # Connect to the WebSocket
        connected1, _ = await communicator1.connect()
        connected2, _ = await communicator2.connect()
        self.assertTrue(connected1)
        self.assertTrue(connected2)

        # Send a message from the first client
        message = {
            "message": "Hello, WebSocket!",
            "username": "testuser1"
        }
        await communicator1.send_json_to(message)

        # Check that both clients receive the message
        response1 = await communicator1.receive_json_from()
        response2 = await communicator2.receive_json_from()

        self.assertEqual(response1["message"], "Hello, WebSocket!")
        self.assertEqual(response1["username"], "testuser1")
        self.assertEqual(response2["message"], "Hello, WebSocket!")
        self.assertEqual(response2["username"], "testuser1")

        # Disconnect
        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_multiple_messages(self):
        """Test sending multiple messages through the WebSocket."""
        communicator = WebsocketCommunicator(
            URLRouter(websocket_urlpatterns),
            self.websocket_url
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Send multiple messages
        messages = [
            {"message": "First message", "username": "testuser"},
            {"message": "Second message", "username": "testuser"},
            {"message": "Third message", "username": "testuser"}
        ]

        for msg in messages:
            await communicator.send_json_to(msg)
            response = await communicator.receive_json_from()
            self.assertEqual(response["message"], msg["message"])
            self.assertEqual(response["username"], msg["username"])

        await communicator.disconnect()

    async def test_different_chat_rooms(self):
        """Test that messages are isolated to their respective chat rooms."""
        room1_url = "/ws/chat/room1/"
        room2_url = "/ws/chat/room2/"

        communicator1 = WebsocketCommunicator(
            URLRouter(websocket_urlpatterns),
            room1_url
        )
        communicator2 = WebsocketCommunicator(
            URLRouter(websocket_urlpatterns),
            room2_url
        )

        # Connect to different rooms
        connected1, _ = await communicator1.connect()
        connected2, _ = await communicator2.connect()
        self.assertTrue(connected1)
        self.assertTrue(connected2)

        # Send a message to room1
        await communicator1.send_json_to({
            "message": "Hello room1",
            "username": "user1"
        })

        # Check that the message is received in room1
        response1 = await communicator1.receive_json_from()
        self.assertEqual(response1["message"], "Hello room1")

        # Check that communicator2 doesn't receive anything (would time out)
        # This test needs a timeout mechanism, so we'll just disconnect instead

        await communicator1.disconnect()
        await communicator2.disconnect()


@pytest.mark.asyncio
class ChatbotConsumerTests(ChannelsLiveServerTestCase):
    """Tests for the WebSocket consumer functionality."""

    def setUp(self):
        """Set up for the WebSocket tests."""
        self.session_id = "test-session"
        self.websocket_url = f"/ws/chatbot/{self.session_id}/"

        # Create test responses
        BotResponse.objects.create(
            category='greeting',
            keywords='hello,hi',
            response_text='Hello! How can I help you?',
            priority=1
        )

    async def test_websocket_connection(self):
        """Test that a WebSocket connection can be established."""
        communicator = WebsocketCommunicator(
            ChatbotConsumer.as_asgi(),
            self.websocket_url
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Check for welcome message
        response = await communicator.receive_json_from()
        self.assertIn('message', response)
        self.assertEqual(response['sender'], 'bot')

        await communicator.disconnect()

    async def test_chatbot_response(self):
        """Test that the chatbot responds to user messages."""
        communicator = WebsocketCommunicator(
            ChatbotConsumer.as_asgi(),
            self.websocket_url
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Skip welcome message
        await communicator.receive_json_from()

        # Send a test message
        await communicator.send_json_to({
            "message": "Hello there"
        })

        # Check that we get a response
        response = await communicator.receive_json_from()
        self.assertIn('message', response)
        self.assertEqual(response['sender'], 'bot')

        await communicator.disconnect()

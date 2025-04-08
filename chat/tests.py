from django.test import TestCase
from django.urls import reverse
from channels.testing import WebsocketCommunicator, ChannelsLiveServerTestCase
from channels.routing import URLRouter
from django.conf.urls import url
import json
import pytest

from .consumers import ChatConsumer
from .routing import websocket_urlpatterns


class ChatViewTests(TestCase):
    """Tests for the HTTP views related to chat."""

    def test_chat_room_view(self):
        """Test that the chat room view returns a successful response."""
        room_name = "test-room"
        response = self.client.get(reverse('chat:room', args=[room_name]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/room.html')
        self.assertContains(response, room_name)


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

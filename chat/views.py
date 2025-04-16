from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatbotSession, BotResponse


def chat_index(request):
    return render(request, "chat/index.html")


def chat_room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


def chatbot_view(request):
    """Render the chatbot interface"""
    # Ensure the user has a session
    if not request.session.session_key:
        request.session.create()

    context = {
        'page_title': 'Floral Couture Chatbot',
        'chatbot_name': 'FloraBot'
    }
    return render(request, "chatbot.html", context)


def chatbot_structure(request):
    """Render only the chatbot HTML structure without JavaScript"""
    # Ensure the user has a session
    if not request.session.session_key:
        request.session.create()

    context = {
        'chatbot_name': 'FloraBot'
    }
    return render(request, "chat/chatbot_structure.html", context)


@login_required
def chat_history(request):
    """View chat history for logged in users"""
    sessions = ChatbotSession.objects.filter(
        customer=request.user.customer
    ).order_by('-created_at')

    context = {
        'page_title': 'Chat History',
        'sessions': sessions
    }
    return render(request, "history.html", context)

from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path("", views.chat_index, name="chat_index"),
    path("room/<str:room_name>/", views.chat_room, name="chat_room"),
    path("chatbot/", views.chatbot_view, name="chatbot"),
    path("chatbot-structure/", views.chatbot_structure, name="chatbot_structure"),
    path("history/", views.chat_history, name="chat_history"),
]

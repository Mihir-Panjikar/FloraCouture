from django.shortcuts import render

# Create your views here.

def chat_room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# chat/views.py
from django.shortcuts import render

@login_required(login_url='signin')
def chat_room(request, recipient_username=None):
    return render(request, 'room.html', {
        'recipient_username': recipient_username
    })
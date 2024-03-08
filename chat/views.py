from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import ChatMessage
import json
from django.db.models import Q

@login_required(login_url='login')
def home(request):
    if request.user.is_health_worker:
        User = get_user_model()
        users = User.objects.all().exclude(id=request.user.id)  # Excluding the current user (health worker)
        admin = User.objects.get(is_admin=True)  # Assuming there's only one admin

        chats = {}
        if request.method == 'GET' and 'admin_id' in request.GET:
            admin_id = request.GET['admin_id']
            chats = ChatMessage.objects.filter(
                (Q(sender=request.user, receiver=admin_id) | Q(sender=admin_id, receiver=request.user))
            ).order_by('date_created')

            context = {
                "page": "home",
                "users": users,
                "admin": admin,
                "chats": chats,
                "chat_id": int(admin_id) if admin_id else 0
            }
            return render(request, "chat.html", context)
        else:
            context = {
                "page": "home",
                "users": users,
                "admin": admin,
                "chats": chats,
                "chat_id": 0
            }
            return render(request, "chat.html", context)

@login_required(login_url='login')
def get_messages(request):
    if request.method == 'POST':
        last_id = request.POST.get('last_id', None)
        chat_id = request.POST.get('chat_id', None)
        
        if last_id and chat_id:
            chats = ChatMessage.objects.filter(
                Q(id__gt=last_id),
                (Q(sender=request.user.id, receiver=chat_id) | Q(sender=chat_id, receiver=request.user.id))
            )
            new_msgs = []
            for chat in chats:
                data = {
                    'id': chat.id,
                    'sender': chat.sender.id,
                    'receiver': chat.receiver.id,
                    'message': chat.message,
                    'date_created': chat.date_created.strftime("%b-%d-%Y %H:%M")
                }
                new_msgs.append(data)
            return HttpResponse(json.dumps(new_msgs), content_type="application/json")
    
    return HttpResponse(status=400)

@login_required(login_url='login')
def send_chat(request):
    if request.method == 'POST':
        post = request.POST
        sender_id = post.get('user_from')
        receiver_id = post.get('user_to')
        message = post.get('message')

        if sender_id and receiver_id and message:
            try:
                sender = get_user_model().objects.get(id=sender_id)
                receiver = get_user_model().objects.get(id=receiver_id)
                new_message = ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)
                return HttpResponse(status=200)
            except Exception as e:
                return HttpResponse(status=500)

    return HttpResponse(status=400)

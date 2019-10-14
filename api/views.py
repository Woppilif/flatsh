from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render
from django.http import HttpResponse
from . import consumers
import json
# Create your views here.

def index(request,pk):
    room_name_json = pk
    return render(request, 'api/chat.html', {"room_name_json":room_name_json})

def index2(request,pk):
    room_name_json = pk
    return render(request, 'api/chat2.html', {"room_name_json":room_name_json})

def index3(request,group_name):
    openDoorAPI(group_name,message = "hello")
    return HttpResponse('<p>Done</p>')

def openDoorAPI(flat_id,message = "hello"):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("chat_{0}".format(flat_id), {
        'type': 'channel_message',
        'message': json.dumps(message)
    })
    return True
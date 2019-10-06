from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render
from django.http import HttpResponse
from . import consumers
# Create your views here.

def index(request,pk):
    room_name_json = pk
    return render(request, 'api/chat.html', {"room_name_json":room_name_json})

def index2(request,pk):
    room_name_json = pk
    return render(request, 'api/chat2.html', {"room_name_json":room_name_json})

def index3(request,group_name):
    message = "hello"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        '{}'.format(group_name),
        {
            'type': 'channel_message',
            'message': message
        }
    )
    '''
    layer = get_channel_layer()
    print(layer.group_send)
    async_to_sync(layer.group_send)('events', {
            'type': 'events.alarm',
            'content': 'triggered'
            })
    '''
    return HttpResponse('<p>Done</p>')
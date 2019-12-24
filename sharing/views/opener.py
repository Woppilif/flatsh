from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render
from django.http import HttpResponse
from sharing import consumers
import json

def openDoorAPI(flat_id,message = "hello",appid='key'):
    print(flat_id,message,appid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("chat_{0}".format(flat_id), {
        'type': 'channel_message',
        'message': json.dumps(message),
        'appid' : appid
    })
    return True

def sendMessageToAllAPI(flat_id,message = "hello"):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("events", {
        'type': 'channel_message',
        'message': json.dumps(message)
    })
    return True
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from flatsharing import settings
from django.views.decorators.csrf import csrf_exempt
import json
from telegram import Bot
from bot_api.modules import wrapper
#from bot_api.modules import prepare, tele
# Create your views here.

@login_required(login_url='/accounts/login/')
def bot_api_update(request):
    bot_set_webhook()
    return HttpResponse("OK")

def bot_set_webhook():
    bot = Bot("705147392:AAFKi_wCIILco9EnoLaykGb3coUWicOueEg")
    bot.setWebhook("https://{0}/bots/telegram/".format(settings.ALLOWED_HOSTS[0]))
    print("https://{0}/bots/telegram/".format(settings.ALLOWED_HOSTS[0]))
    return True

@csrf_exempt
def telegram(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        wr = wrapper.Wrapper(json_data)
        wr.start()
        return HttpResponse('OK',status=200)
    return HttpResponse('Method not allowed',status=405)




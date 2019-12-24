from django.shortcuts import render, get_object_or_404, redirect
from sharing.models import Flats, Rents, Access, Payments, Favorites
from rents.forms import CustomUserCreationForm, RentForm, UserDocumentsForm, UploadFileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
import time
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from sharing import consumers
import json
from sharing.views.opener import openDoorAPI
from django.views.decorators.csrf import csrf_exempt
import os
def checkdocs(function):
    '''
        Redirect user to booked object if he has one
    '''
    def decorator(request, *args, **kwargs):
        if request.user.usersdocuments.firstname != "":
            return redirect('rents:card')
        return function(request, *args, **kwargs)
    return decorator

def checkcard(function):
    '''
        Redirect user to booked object if he has one
    '''
    def decorator(request, *args, **kwargs):
        if request.user.usersdocuments.firstname == "":
            return redirect('rents:bot')
        if request.user.usersdocuments.yakey is None:
            return redirect('rents:card')
        return function(request, *args, **kwargs)
    return decorator

def sendToBuchen(function):
    '''
        Redirect user to booked object if he has one
    '''
    def decorator(request, *args, **kwargs):
        r = Rents.objects.filter(rentor=request.user,paid=False,status=True).first()
        if r:
            return redirect('rents:openpay',pk=r.pk)
        return function(request, *args, **kwargs)
    return decorator

def sendToRenta(function):
    '''
        Redirect to current renta object 
    '''
    def decorator(request, *args, **kwargs):
        r = Rents.objects.filter(rentor=request.user,paid=True,status=True).first()
        if r:
            return redirect('rents:opendoor',pk=r.pk)
        return function(request, *args, **kwargs)
    return decorator

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('rents:map')
    return render(request, 'index.html',{})

def registration(request):
    if request.user.is_authenticated:
        return redirect('rents:map')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user, password = form.save()
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect('rents:bot')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registration.html',{'form': form})

@login_required(login_url='/accounts/login/')
@checkcard
@sendToRenta
@sendToBuchen
def map(request):
    flats = Flats.objects.filter(door_status=True,status='U')
    if request.GET.get('q') is not None:
        flats = flats.filter(price__gte=request.GET.get('q'))
    today = timezone.now()
    tomorrow = today + timedelta(days=1)
    return render(request, 'map.html',{"flats":flats,"today":str(today.strftime("%Y-%m-%dT%H:%M")),"tomorrow":str(tomorrow.strftime("%Y-%m-%dT%H:%M"))})

@login_required(login_url='/accounts/login/')
@checkcard
@sendToRenta
def act(request,pk):
    renta = get_object_or_404(Rents, pk=pk,rentor=request.user,paid=False)
    if request.method == 'POST':
        if "pay" in request.POST:
            deposit = Payments.paym.createPayment(renta=renta,p_type=1)
            print("Renta deposit obj created {0}".format(deposit))
            full = Payments.paym.createPayment(renta=renta,p_type=2)
            print("Renta payment obj created {0}".format(full))
            access, created = Access.access.createPaidAccess(full.renta)
            print("And access {0}".format(access))
            return redirect('rents:opendoor',pk=renta.pk)
        if "cancel" in request.POST:
            renta.status = None
            renta.save()
            return redirect('rents:map')
        if "open" in request.POST:
            return redirect('rents:access')
    return render(request, 'act.html',{"renta":renta})

@login_required(login_url='/accounts/login/')
@checkcard
@sendToRenta
def actpay(request,pk):
    renta = get_object_or_404(Rents, pk=pk,rentor=request.user,paid=False)
    if request.method == 'POST':
        if "pay" in request.POST:
            deposit = Payments.paym.createPayment(renta=renta,p_type=1)
            print("Renta deposit obj created {0}".format(deposit))
            full = Payments.paym.createPayment(renta=renta,p_type=2)
            print("Renta payment obj created {0}".format(full))
            access, created = Access.access.createPaidAccess(full.renta)
            print("And access {0}".format(access))
            return redirect('rents:opendoor',pk=renta.pk)
        if "cancel" in request.POST:
            renta.status = None
            renta.save()
            return redirect('rents:map')
    return render(request, 'actpay.html',{"renta":renta})

@login_required(login_url='/accounts/login/')
@checkcard
@sendToRenta
@sendToBuchen
def apartment(request,pk):
    flat = get_object_or_404(Flats, pk=pk)
    today = timezone.now()
    tomorrow = today + timedelta(days=1)
    if request.method == 'POST':
        form = RentForm(data=request.POST, current_flat=flat, rentor= request.user)
        if form.is_valid():
            renta = form.save()
            return redirect('rents:openpay',pk=renta.pk)
        else:
            return render(request, 'apartment.html',{"form":form,"flat":flat,"today":str(today.strftime("%Y-%m-%dT%H:%M")),"tomorrow":str(tomorrow.strftime("%Y-%m-%dT%H:%M"))})
    return render(request, 'apartment.html',{"flat":flat,"today":str(today.strftime("%Y-%m-%dT%H:%M")),"tomorrow":str(tomorrow.strftime("%Y-%m-%dT%H:%M"))})

@login_required(login_url='/accounts/login/')
@checkcard
def favorites(request):
    flats = Favorites.objects.filter(user=request.user)
    if request.GET.get('price') is not None:
        if request.GET.get('price') == "up":
            flats = flats.order_by('flat__price')
        elif request.GET.get('price') == "down":
            flats = flats.order_by('-flat__price')
    flats = [i.flat for i in flats]
    return render(request, 'favorites.html',{"flats":flats})

@login_required(login_url='/accounts/login/')
@checkcard
def favoritesAdd(request,pk):
    obj, created = Favorites.objects.get_or_create(
        user = request.user,
        flat_id = pk 
    )
    if created is False:
        obj.delete()
    return redirect('rents:apartment',pk=pk)

@login_required(login_url='/accounts/login/')
@checkcard
@sendToRenta
@sendToBuchen
def lists(request):
    flats = Flats.objects.filter(door_status=True,status='U')
    if request.GET.get('price') is not None:
        if request.GET.get('price') == "up":
            flats = flats.order_by('price')
        elif request.GET.get('price') == "down":
            flats = flats.order_by('-price')
    return render(request, 'list.html',{"flats":flats})

@login_required(login_url='/accounts/login/')
@checkcard
def opendoor(request,pk):
    renta = get_object_or_404(Rents, pk=pk,rentor=request.user,paid=True,status=True)
    if request.method == 'POST':
        if "open" in request.POST:
            return redirect('rents:access')
        if "end" in request.POST:
            Payments.objects.get(renta=renta,rentor=request.user,payment_type=1).cancel()
            renta.status = None
            renta.save()
            return redirect('rents:map')
    return render(request, 'opendoor.html',{"renta":renta})

@login_required(login_url='/accounts/login/')
@checkcard
@sendToRenta
def openpay(request,pk):
    renta = get_object_or_404(Rents, pk=pk,rentor=request.user,paid=False)
    if request.method == 'POST':
        if "pay" in request.POST:
            return redirect('rents:actpay',pk=renta.pk)
        if "cancel" in request.POST:
            renta.status = None
            renta.save()
            return redirect('rents:map')
        if "open" in request.POST:
            return redirect('rents:act',pk=renta.pk)
    return render(request, 'openpay.html',{"renta":renta,"flat":renta.flat})

@login_required(login_url='/accounts/login/')
@checkcard
def options(request):
    rents = Rents.objects.filter(rentor=request.user).order_by('-id')[:10]
    payments = Payments.objects.filter(rentor=request.user).order_by('-id')[:10]
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            return redirect('rents:options')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'options.html', {'form': form,'rents':rents,'payments':payments})

@login_required(login_url='/accounts/login/')
def card(request,code = None):
    try:
        print(request.user.usersdocuments)
    except:
        return redirect('rents:bot')
    if code is not None:
        if code == "delete":
            request.user.usersdocuments.yakey = None
            request.user.usersdocuments.ya_card_type = None
            request.user.usersdocuments.ya_card_last4 = None
            request.user.usersdocuments.save()
            return redirect('rents:map')
        payment_obj = get_object_or_404(Payments, pk=int(code))
        payment = payment_obj.get()
        if payment.status == 'waiting_for_capture':
            request.user.usersdocuments.yakey = payment.payment_method.id
            request.user.usersdocuments.ya_card_type = payment.payment_method.card.card_type
            request.user.usersdocuments.ya_card_last4 = payment.payment_method.card.last4
            request.user.usersdocuments.save()
            payment_obj.cancel()
            return redirect('rents:map')
        else:
            return render(request, 'payment.html', {})  
    if request.method == 'POST':
        payment_object = Payments.paym.createPayment(None,p_type=0,user=request.user)
        return redirect(payment_object.confirmation.confirmation_url)
    else:
        return render(request, 'payment.html', {})  

@login_required(login_url='/accounts/login/')
@checkdocs
def bot(request):
    if request.method == 'POST':
        form = UserDocumentsForm(data=request.POST, files=request.FILES,instance=request.user.usersdocuments)
        if form.is_valid():
            docs = form.save(commit=False)
            #docs.user = request.user
            docs.save()
            print("D|: {0}".format(docs))
            usr = request.user
            usr.first_name = docs.firstname
            usr.last_name = docs.lastname
            usr.save()
            
            return redirect('rents:card')
    else:
        form = UserDocumentsForm()
    return render(request, 'documents.html', {'form': form})

@login_required(login_url='/accounts/login/')
def access(request):
    renta = Rents.objects.filter(rentor=request.user,status=True).first()
    acc = renta.AccessObj() #get_object_or_404(Access, pk=pk,user=request.user)
    print(acc)
    acc.setStartTime()
    if acc.CheckAccess():
        print("Signal sent to {0}".format(renta.flat.id))
        acc.usedAdd()
        openDoorAPI(renta.flat.id,'open',renta.flat.app_id)
    else:
        print("Rights expired!")
    return redirect('rents:act',pk=renta.pk)

def trial_renta(request, trial_key):
    renta = get_object_or_404(Rents, trial_key=trial_key,status=True,paid=True)
    if request.method == 'POST':
        if "open" in request.POST:
            return redirect('rents:trial_access',trial_key=trial_key)
    return render(request, 'opendoor_trial.html',{"renta":renta})

def trial_access(request,trial_key):
    renta = Rents.objects.filter(trial_key=trial_key,status=True).first()
    acc = renta.AccessObj() #get_object_or_404(Access, pk=pk,user=request.user)
    print(acc)
    acc.setStartTime()
    if acc.CheckAccess():
        print("Signal sent to {0}".format(renta.flat.id))
        acc.usedAdd()
        openDoorAPI(renta.flat.id,'open',renta.flat.app_id)
    else:
        print("Rights expired!")
    return redirect('rents:trial_renta',trial_key=trial_key)

def handle_uploaded_file(f):
    with open(os.path.join('media/flats/images', "hello.txt"), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        #form = UploadFileForm(request.POST, request.FILES)
        #if form.is_valid():
        handle_uploaded_file(request.FILES['file'])
        return HttpResponse("OK",status=201)
    return HttpResponse("nO",status=200)

def user_agreement(request):
    return render(request, 'documents/user_agreement.html',{})

def agreement(request):
    return render(request, 'documents/agreement.html',{})
from django.shortcuts import render, get_object_or_404, redirect
from sharing.models import Flats, Rents, Access, Payments, Favorites, UsersDocuments, Devices, SystemLogs
from rents.forms import CustomUserCreationForm, RentForm, UserDocumentsForm, UploadFileForm, RentaPayForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from datetime import timedelta, datetime
from django.http import HttpResponse, JsonResponse
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
from django.db.models import Max, Min
from django.template.loader import render_to_string
from django.core import serializers
from django.contrib import messages
import hashlib
from yandex_checkout import Payment,Configuration 
from django.conf import settings
from rents.modules import bitx

Configuration.account_id = settings.YA_ACCOUNT_ID
Configuration.secret_key = settings.YA_SECRET_KEY

def checkdocs(function):
    '''
        Redirect user to booked object if he has one
    '''
    def decorator(request, *args, **kwargs):
        '''
        if request.user.usersdocuments.firstname != "":
            return redirect('rents:card_oper')
        '''
        return function(request, *args, **kwargs)
    return decorator

def checkcard(function):
    '''
        Redirect user to booked object if he has one
    '''
    def decorator(request, *args, **kwargs):
        try:
            if request.user.usersdocuments.firstname == "":
                return redirect('rents:bot')
            '''
            if request.user.usersdocuments.yakey is None:
                return redirect('rents:card_oper')
            '''
        except:
            UsersDocuments.objects.create(
                user=request.user,
                phone_number = 000
            )
            return redirect('rents:bot')
        return function(request, *args, **kwargs)
    return decorator

def sendToBuchen(function):
    '''
        Redirect user to booked object if he has one
    '''
    def decorator(request, *args, **kwargs):
        r = Rents.objects.filter(rentor=request.user,paid=False,status=True).first()
        if r:
            return redirect('rents:act',pk=r.pk)
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

def flatsFilter(flats,request):
    if request.GET.get('price') is not None:
        if request.GET.get('price') == "up":
            flats = flats.order_by('price')
        elif request.GET.get('price') == "down":
            flats = flats.order_by('-price')
    if request.GET.get('max') is not None and request.GET.get('min') is not None:
        flats = flats.filter(price__gte=request.GET.get('min'),price__lte=request.GET.get('max'))
    if request.GET.get('rooms') is not None:
        flats = flats.filter(rooms=int(request.GET.get('rooms')))
    if request.GET.get('start') is not None and request.GET.get('end') is not None:
        flat_list = []
        for i in flats:
            start = timezone.make_aware(datetime.strptime(request.GET.get('start'), '%Y-%m-%d'))
            end = timezone.make_aware(datetime.strptime(request.GET.get('end'), '%Y-%m-%d'))
            renta = Rents.objects.filter(flat=i,start__gte=start,end__lte=end,status=True,paid=True).last()
            if renta is None:
                flat_list.append(i)
        flats = flat_list
    return flats


@login_required(login_url='/accounts/login/')
@checkcard
@sendToRenta
@sendToBuchen
def lists(request):
    data = dict()
    flats = Flats.objects.filter(door_status=True,status='U')
    today = timezone.now().replace(hour=14,minute=0)
    tomorrow = (today + timedelta(days=1)).replace(hour=12,minute=0)
    max_val = flats.aggregate(Max('price')) 
    min_val = flats.aggregate(Min('price')) 
    
    data['today'] = str(today.strftime("%Y-%m-%dT%H:%M"))
    data['tomorrow'] = str(tomorrow.strftime("%Y-%m-%dT%H:%M"))
    data['max'] = int(max_val['price__max'])
    data['min'] = int(min_val['price__min'])
    data['max_val'] = data['max']
    data['min_val'] = data['min']
    if len(request.GET.keys()) > 0:
        flats = flatsFilter(flats,request)
        data['form_is_valid'] = True
        #data['flats'] = [(flaat.pk,flaat.latitude, flaat.longitude) for flaat in flats] #serializers.serialize('json', flats)
        data['max_val'] = request.GET.get('max')
        data['min_val'] = request.GET.get('min')
        data['html_book_list'] = render_to_string('list_part.html', {
                'flats':flats
            })
        if request.GET.get('api') is not None:
            return JsonResponse(data)

    if request.GET.get('price') is not None:
        if request.GET.get('price') == "up":
            flats = flats.order_by('price')
        elif request.GET.get('price') == "down":
            flats = flats.order_by('-price')
    data['flats'] = flats
    return render(request, 'list.html',data)

@login_required(login_url='/accounts/login/')
@checkcard
@sendToRenta
@sendToBuchen
def map(request):
    data = dict()
    flats = Flats.objects.filter(door_status=True,status='U')
    today = timezone.now().replace(hour=14,minute=0)
    tomorrow = (today + timedelta(days=1)).replace(hour=12,minute=0)
    max_val = flats.aggregate(Max('price')) 
    min_val = flats.aggregate(Min('price')) 
    
    data['today'] = str(today.strftime("%Y-%m-%dT%H:%M"))
    data['tomorrow'] = str(tomorrow.strftime("%Y-%m-%dT%H:%M"))
    data['max'] = int(max_val['price__max'])
    data['min'] = int(min_val['price__min'])
    data['max_val'] = data['max']
    data['min_val'] = data['min']
    if len(request.GET.keys()) > 0:
            flats = flatsFilter(flats,request)
            data['form_is_valid'] = True
            data['flats'] = [(flaat.pk,flaat.latitude, flaat.longitude) for flaat in flats] #serializers.serialize('json', flats)
            data['max_val'] = request.GET.get('max')
            data['min_val'] = request.GET.get('min')
            if request.GET.get('api') is not None:
                return JsonResponse(data)
    data['flats'] = flats
    return render(request, 'map.html',data)

@login_required(login_url='/accounts/login/')
@checkcard
@sendToRenta
def act(request,pk):
    renta = get_object_or_404(Rents, pk=pk,rentor=request.user,paid=False)
    if request.method == 'POST':
        if "pay" in request.POST:
            return redirect('rents:pay',pk=renta.pk)
            '''
            form = RentaPayForm(renta=renta)
            if form.is_valid():
                return redirect('rents:opendoor',pk=form.save())
            '''
        if "cancel" in request.POST:
            renta.status = None
            renta.save()
            return redirect('rents:map')
        if "open" in request.POST:
            return redirect('rents:access')
    return render(request, 'act.html',{"renta":renta,"date":timezone.now()})

@login_required(login_url='/accounts/login/')
@checkcard
@sendToRenta
@sendToBuchen
def apartment(request,pk):
    flat = get_object_or_404(Flats, pk=pk)
    today = timezone.make_naive(timezone.now())
    tomorrow = today + timedelta(days=1)
    rentaObj = Rents.objects.filter(flat=flat,start__gte=timezone.now(),status=True,paid=True).last()
    print(rentaObj)
    
    untill = daysBeforeFirstRenta(flat,today)
    if request.method == 'POST':
        form = RentForm(data=request.POST, current_flat=flat, rentor= request.user)
        if form.is_valid():
            renta = form.save()
            return redirect('rents:act',pk=renta.pk)
        else:
            return render(request, 'apartment.html',{"form":form,"flat":flat,"today":str(today.strftime("%Y-%m-%dT%H:%M")),"tomorrow":str(tomorrow.strftime("%Y-%m-%dT%H:%M"))})
    elif request.method == 'GET' and len(request.GET.keys()) > 0:
        data = dict()
        data['days'] = daysBeforeFirstRenta(flat,datetime.strptime(request.GET.get('date'), '%Y-%m-%d'))
        return JsonResponse(data)
    return render(request, 'apartment.html',{"untill":untill,"flat":flat,"today":str(today.strftime("%Y-%m-%dT%H:%M")),"tomorrow":str(tomorrow.strftime("%Y-%m-%dT%H:%M"))})

def daysBeforeFirstRenta(flat,date):
    date = date.replace(hour=14,minute=0)
    current = flat.getCurrentRenta(timezone.make_aware(date))
    if current is not None:
        return 0
    else:
        first = flat.getFirstFutureRenta(timezone.make_aware(date))
        if first is not None:
            return abs((date - timezone.make_naive(first.start)).days)
        else:
            return 100
    
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
        messages.success(request, 'Удалено из избранных')
    else:
        messages.success(request, 'Добавлено в избранное')
    return redirect('rents:apartment',pk=pk)



@login_required(login_url='/accounts/login/')
@checkcard
def opendoor(request,pk):
    renta = get_object_or_404(Rents, pk=pk,rentor=request.user,paid=True,status=True)
    if request.method == 'POST':
        if "open" in request.POST:
            return redirect('rents:access')
        if "end" in request.POST:
            #Payments.objects.get(renta=renta,rentor=request.user,payment_type=1).cancel()
            renta.status = None
            renta.save()
            return redirect('rents:map')
    return render(request, 'opendoor.html',{"renta":renta})

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
        print(code)         
        payment_obj = get_object_or_404(Payments, payment_id=code)
        payment = payment_obj.get()
        request.user.usersdocuments.addCard(payment)
        payment_obj.setInfo(payment_obj.cancel())
        return redirect('rents:map')


    elif request.method == 'POST':
        request.user.usersdocuments.deleteCard()
        return redirect('rents:map')    
    else:
        data = dict()
        paymentObj, created = Payments.objects.get_or_create(
            rentor = request.user,
            renta = None,
            price = 1,
            payment_type = 0,
            status = False,
        )

        if created is True:
            paymentObj.date = timezone.now()
            yandex = paymentObj.createPaymentObject()
            paymentObj.setInfo(yandex)
            data['payment'] = yandex
            data['id'] = paymentObj.payment_id
        else:
            data['payment'] = paymentObj.findOne()
            data['id'] = paymentObj.payment_id

        return render(request, 'payment.html', data)  

@login_required(login_url='/accounts/login/')
@checkdocs
def pay(request,pk):
    renta = get_object_or_404(Rents, pk=pk,rentor=request.user,paid=False)
    if renta.paid is False:
        paymentObj = Payments.objects.filter(renta=renta,payment_type = 2).first()
        if paymentObj is not None:
            paymentObj.setInfo(paymentObj.findOne()).setStatus().rentaPaid()
            if paymentObj.status is True:
                access, created = Access.access.createPaidAccess(paymentObj.renta)
                return redirect('rents:opendoor',pk=renta.pk)

        data = dict()
        data['renta'] = renta
        paymentObj, created = Payments.objects.get_or_create(
            rentor = renta.rentor,
            renta = renta,
            price = renta.getPrice(),
            payment_type = 2,
            status = False,
        )
        if created is True:
            paymentObj.date = timezone.make_naive(timezone.now())
            yandex = paymentObj.createPaymentObject(capture = True, save_payment_method = False)
            paymentObj.setInfo(yandex)
            data['payment'] = yandex
        else:
            data['payment'] = paymentObj.findOne()
        return render(request, 'pay.html',data)
    else:
        return redirect('rents:opendoor',pk=renta.pk)



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
            
            return redirect('rents:map')
    else:
        form = UserDocumentsForm()
    return render(request, 'documents.html', {'form': form})

@login_required(login_url='/accounts/login/')
def access(request):
    renta = Rents.objects.filter(rentor=request.user,status=True).first()
    acc = renta.AccessObj()
    print(acc)
    acc.setStartTime()
    if acc.CheckAccess():
        print("Signal sent to {0}".format(renta.flat.id))
        acc.usedAdd()
        openDoorAPI(renta.flat.device.id,'open',renta.flat.device.secret_key)
    else:
        print("Rights expired!")
    return redirect('rents:act',pk=renta.pk)

def trial_pay(request, trial_key):
    renta = get_object_or_404(Rents, trial_key=trial_key,status=True)
    if renta.paid is False:
        data = dict()
        paymentObj, created = Payments.objects.get_or_create(
            rentor = renta.rentor,
            renta = renta,
            price = renta.getPrice(),
            payment_type = 3,
            status = False,
        )
        data['renta'] = renta
        if created is True:
            paymentObj.date = timezone.make_naive(timezone.now())
            yandex = paymentObj.createPaymentObject(capture = True, save_payment_method = False)
            paymentObj.setInfo(yandex)
            data['payment'] = yandex
        else:
            data['payment'] = paymentObj.findOne()
        return render(request, 'pay.html',data)
    else:
        return redirect('rents:trial_renta',trial_key=trial_key)

def trial_renta(request, trial_key):
    renta = get_object_or_404(Rents, trial_key=trial_key,status=True)
    if renta.paid is False:
        paymentObj = Payments.objects.filter(renta=renta,payment_type = 3).first()
        if paymentObj is not None:
            paymentObj.setInfo(paymentObj.findOne()).setStatus().rentaPaid()
            if paymentObj.status is True:
                access, created = Access.access.createPaidAccess(paymentObj.renta)
        return redirect('rents:trial_pay',trial_key=trial_key)
    if request.method == 'POST':
        if "open" in request.POST:
            return redirect('rents:trial_access',trial_key=trial_key)
    return render(request, 'opendoor_trial.html',{"renta":renta})

def trial_access(request,trial_key):
    renta = Rents.objects.filter(trial_key=trial_key,status=True,paid=True).first()
    acc = renta.AccessObj() #get_object_or_404(Access, pk=pk,user=request.user)
    print(acc)
    acc.setStartTime()
    if acc.CheckAccess():
        print("Signal sent to {0}".format(renta.flat.id))
        acc.usedAdd()
        openDoorAPI(renta.flat.device.id,'open',renta.flat.device.secret_key)
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

def device(request,dkey):
    obj, created = Devices.objects.get_or_create(
        open_key = dkey
    )
    if created is True:
        data = dict()
        code = hashlib.md5()
        codex = "{0}{1}".format(dkey,obj.pk)
        code.update(codex.encode())
        obj.secret_key = code.hexdigest()
        obj.created_at = timezone.now()
        obj.save()
        data["id"] = obj.pk
        return JsonResponse(data,status=200)

@csrf_exempt
def bitx_data(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        flat = Flats.objects.get(bxcal_id=int(json_data['id']))
        soap = bitx.Soap()
        data = soap.getByInternalId(flat.internal_id)
        for i in data:
            r = soap.parse_data(i)
            print(r)
        return HttpResponse("OK",status=200)
    return HttpResponse("nO",status=200)
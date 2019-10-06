from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from yandex_checkout import Payment,Configuration 
import uuid
import time
from django.template.loader import render_to_string
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
Configuration.account_id = 591310

Configuration.secret_key = "test_1J9BQa-AGyxrN3U9x7CrJ6l4bM0ri8L5a5aGcBj7T_w"

def index(request):
    return redirect('/accounts/login/')

@login_required(login_url='/accounts/login/')
def UserPage2(request):
    flats = Flats.objects.filter()
    return render(request, 'flats/flats_map.html', {"flats":flats})

def UserPage(request):
    #print(request.user.partners.CheckUserPartner())
    #print(request.user.workers.CheckUserWorker())
    print(request.user.first_name == "")
    now = timezone.now()
    try:
        print(request.user.usersdocuments.yakey)
    except:
        return redirect('user:userDocuments')
    if request.user.usersdocuments.status is False:
        messages.warning(request,"Ваш аккаунт еще не активирован!")
    flats = Flats.objects.filter()
    renta = Rents.objects.filter(rentor=request.user,end__gte=now,start__lt=now,status__isnull=False).last()
    payments = Payments.objects.filter(renta=renta).last()
    return render(request, 'flats/flats_map.html', {"renta":renta,"payment":payments,"flats":flats})

def addCard2(request):
    payment = Payment.create({
    "amount": {
        "value": "100.00",
        "currency": "RUB"
    },
    "payment_method_id": "2521c2e3-000f-5000-a000-15bb9a95a0f4",
    "description": "Заказ №105"
    })
    print(payment.status)
    idempotence_key = str(uuid.uuid4())
    response = Payment.capture(
            payment.id,
            {
                "amount": {
                "value": 100,
                "currency": "RUB"
                }
            },
            idempotence_key
            )
    print(response.status)
    return HttpResponse()

def addCard(request):
    payment, created = Payments.objects.get_or_create(
        rentor = request.user,
        renta_id = None,
        price = 2,
        date = timezone.now(),
        payment_type = 'D'
    )
    idempotence_key = str(uuid.uuid4())
    session_key = str(uuid.uuid4())
    payment_object = Payment.create({
        "amount": {
        "value": payment.price,
        "currency": "RUB"
        },
        "payment_method_data": {
        "type": "bank_card"
        },
        #"refundable": "true",
        #"capture":"false",
        "confirmation": {
        "type": "redirect",
        "return_url": "http://{0}/pay/order/{1}".format('127.0.0.1:8000',payment.pk)
        },
        "description": "Заказ ID:{0}".format(payment.pk),
        "save_payment_method": "true"
    }, idempotence_key)
    payment.payment_id = payment_object.id
    payment.payment_status = payment_object.status
    payment.created_at = payment_object.created_at
    payment.expires_at = payment_object.expires_at
    payment.save()
    return redirect(payment_object.confirmation.confirmation_url)

def flatPayDeposit(request,pk):
    payment, created = Payments.objects.get_or_create(
        rentor = request.user,
        renta_id = pk,
        price = 1000,
        date = timezone.now(),
        payment_type = 'D'
    )
    #payment = get_object_or_404(Payments, pk=pk,rentor=request.user,status=False)
    idempotence_key = str(uuid.uuid4())
    session_key = str(uuid.uuid4())
    payment_object = Payment.create({
        "amount": {
        "value": payment.price,
        "currency": "RUB"
        },
        "payment_method_data": {
        "type": "bank_card"
        },
        #"refundable": "true",
        #"capture":"false",
        "confirmation": {
        "type": "redirect",
        "return_url": "http://{0}/pay/order/{1}".format('127.0.0.1:8000',payment.pk)
        },
        "description": "Заказ ID:{0}".format(payment.pk)
    }, idempotence_key)
    payment.payment_id = payment_object.id
    payment.payment_status = payment_object.status
    payment.created_at = payment_object.created_at
    payment.expires_at = payment_object.expires_at
    payment.save()
    return redirect(payment_object.confirmation.confirmation_url)

def flatPayRenta(request,pk):
    payment, created = Payments.objects.get_or_create(
        rentor = request.user,
        renta_id = pk,
        price = 1000,
        date = timezone.now(),
        payment_type = 'F'
    )
    #payment = get_object_or_404(Payments, pk=pk,rentor=request.user,status=False)
    idempotence_key = str(uuid.uuid4())
    session_key = str(uuid.uuid4())
    payment_object = Payment.create({
        "amount": {
        "value": payment.price,
        "currency": "RUB"
        },
        "payment_method_data": {
        "type": "bank_card"
        },
        "confirmation": {
        "type": "redirect",
        "return_url": "http://{0}/pay/order/{1}".format('127.0.0.1:8000',payment.pk)
        },
        "description": "Заказ ID:{0}".format(payment.pk)
    }, idempotence_key)
    payment.payment_id = payment_object.id
    payment.payment_status = payment_object.status
    payment.created_at = payment_object.created_at
    payment.expires_at = payment_object.expires_at
    payment.save()
    return redirect(payment_object.confirmation.confirmation_url)

def OnPaymentCallback(request,pk):
    user_payments = get_object_or_404(Payments, pk=pk,rentor=request.user)
    payment = Payment.find_one(user_payments.payment_id)
    print(payment.status)
    if payment.status == 'waiting_for_capture' and user_payments.payment_type=='D':
        print(payment.payment_method.id)
        user_payments.payment_status = payment.status
        user_payments.created_at = payment.created_at
        user_payments.expires_at = payment.expires_at
        user_payments.captured_at = payment.captured_at
        user_payments.status = True
        user_payments.save()
        acc = Access.objects.create(
            user = request.user,
            renta = user_payments.renta
        )
        print('Yeah its D')
    elif payment.status == 'waiting_for_capture' and user_payments.payment_type=='F':
        idempotence_key = str(uuid.uuid4())
        response = Payment.capture(
            user_payments.payment_id,
            {
                "amount": {
                "value": user_payments.price,
                "currency": "RUB"
                }
            },
            idempotence_key
            )

        user_payments.payment_status = response.status
        user_payments.created_at = payment.created_at
        user_payments.expires_at = payment.expires_at
        user_payments.captured_at = payment.captured_at
        user_payments.status = True
        user_payments.save()
        
        acc = Access.objects.create(
            user = request.user,
            renta = user_payments.renta,
            start = user_payments.renta.start,
            end = user_payments.renta.end
        )
        print('Yeah its F')
    
    return redirect('sharing:user')

def access(request,pk):
    acc = get_object_or_404(Access, pk=pk,user=request.user)
    #print(acc.get_absolute_url())
    acc.setStartTime()
    if acc.CheckAccess():
        print("Signal sent")
        acc.usedAdd()
    else:
        print("Rights expired!")

    return redirect('sharing:user')

def test(request):
    while True:
        if a== 1:
            return JsonResponse({})
        time.sleep(12)
        return JsonResponse({})

def rentCancel(request,pk):
    payment_object = get_object_or_404(Payments,rentor=request.user,status=True,renta_id = pk,payment_status='waiting_for_capture')
    idempotence_key = str(uuid.uuid4())
    response = Payment.cancel(
        payment_object.payment_id,
        idempotence_key
    )
    print(response.status)
    payment_object.renta.status = None
    payment_object.renta.save()
    return redirect('sharing:user')

@csrf_exempt
def UserRegister(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('sharing:user')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@csrf_exempt
def UserDocuments(request):
    if request.method == 'POST':
        form = UserDocumentsForm(data=request.POST, files=request.FILES)
        if form.is_valid():

            docs = form.save(commit=False)
            docs.user = request.user
            docs.save()
            return redirect('sharing:user')
    else:
        form = UserDocumentsForm()
    return render(request, 'user/documents.html', {'form': form})

def flatInfo(request,pk):
    flat = get_object_or_404(Flats, pk=pk)
    images = Images.objects.filter(flat=flat)
    data = dict()
    data['html_book_list'] = render_to_string('flats/includes/partial_book_list.html', {
                'flat':flat,'images':images
    })
  
    data['form_is_valid'] = True
    return JsonResponse(data)

def startRent(request,pk):
    flat = get_object_or_404(Flats, pk=pk)
    data = dict()
    form = RentForm(instance=flat)
    data['html_book_list'] = render_to_string('flats/includes/rent_create.html', {
                'flat':flat,'form':form
    })
  
    data['form_is_valid'] = True
    return JsonResponse(data)

@csrf_exempt
def flatsFilter(request):
    data = dict()
    if request.method == 'POST':
        form = RentSearchForm(request.POST)
        print(form)
        print("Ok!")
    else:
        form = RentSearchForm()
    data['html_book_list'] = render_to_string('flats/includes/flats_filter.html', {
                    'form':form
        })
    data['form_is_valid'] = True
    return JsonResponse(data) 

@login_required(login_url='/accounts/login/')
def worker_update(request, user_id):
    book = get_object_or_404(BotUsersAccounts, id=user_id)
    if request.method == 'POST':
        form = BotUsersAccountsForm(data=request.POST, instance=book,current_user=request.user)
    else:
        form = BotUsersAccountsForm(instance=book,current_user=request.user)
    return save_book_form(request, form, 'workers/includes/partial_book_update.html')


    





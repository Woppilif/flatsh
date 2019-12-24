from django.shortcuts import render, get_object_or_404, redirect
from yandex_checkout import Payment,Configuration 
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login#
from django.contrib import messages
from sharing.models import Payments, Rents
from django.utils import timezone
from flatsharing.settings import ALLOWED_HOSTS
Configuration.account_id = 591310

Configuration.secret_key = "test_1J9BQa-AGyxrN3U9x7CrJ6l4bM0ri8L5a5aGcBj7T_w"


# Create your views here.
@login_required(login_url='/accounts/login/')
def UserSettingsMenu(request):
    rents = Rents.objects.filter(rentor=request.user)
    payments = Payments.objects.filter(rentor=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш пароль был успешно обновлен!')
            #create_log(request.user,'Обновление пароля')
            return redirect('user:settings')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/settings.html', {'form': form,'rents':rents,'payments':payments})

@login_required(login_url='/accounts/login/')
def deletecard(request):
    request.user.usersdocuments.yakey = None
    request.user.usersdocuments.ya_card_type = None
    request.user.usersdocuments.ya_card_last4 = None
    request.user.usersdocuments.save()
    return redirect('projects:list')

@login_required(login_url='/accounts/login/')
def UserDocuments(request):
    if request.method == 'POST':
        form = UserDocumentsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            docs = form.save(commit=False)
            docs.user = request.user
            docs.save()
            print(docs.firstname)
            usr = request.user
            usr.first_name = docs.firstname
            usr.last_name = docs.lastname
            usr.save()
            return redirect('user:UserAddCard')
    else:
        form = UserDocumentsForm()
    return render(request, 'user/documents.html', {'form': form})

@login_required(login_url='/accounts/login/')
def UserAddCard(request):
    try:
        print(request.user.usersdocuments)
    except:
        return redirect('user:userDocuments')
    if request.method == 'POST':
        payment_object = Payments.paym.createPayment(None,p_type=0,user=request.user)
        return redirect(payment_object.confirmation.confirmation_url)
    else:

        return render(request, 'user/payment.html', {})

@login_required(login_url='/accounts/login/')
def UserAddCardConfirm(request):
    try:
        if request.user.usersdocuments.yakey is not None:
            return redirect('projects:list')
    except:
        return redirect('user:userDocuments')
    payment_obj = Payments.objects.filter(rentor=request.user,payment_type = 0).last()
    payment = Payment.find_one(payment_obj.payment_id)
    if payment.status == 'waiting_for_capture':
        print(payment.payment_method.id)
        request.user.usersdocuments.yakey = payment.payment_method.id
        request.user.usersdocuments.ya_card_type = payment.payment_method.card.card_type
        request.user.usersdocuments.ya_card_last4 = payment.payment_method.card.last4
        request.user.usersdocuments.save()
        idempotence_key = str(uuid.uuid4())
        response = Payment.capture(
            payment.id,
            {
                "amount": {
                "value": 1,
                "currency": "RUB"
                }
            },
            idempotence_key
        )
        return redirect('projects:list')
    return render(request, 'user/payment.html', {})

def UserRegister(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('projects:list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
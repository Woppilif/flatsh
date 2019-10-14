from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserDocumentsForm
from yandex_checkout import Payment,Configuration 
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth import authenticate, login#
from django.contrib import messages
from sharing.models import Payments, Rents
from django.utils import timezone
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
def UserDocuments(request):
    if request.method == 'POST':
        form = UserDocumentsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            docs = form.save(commit=False)
            docs.user = request.user
            if docs.agreement is True:
                docs.save()
                return redirect('user:UserAddCard')
            messages.warning(request,"Вы не можете быть зарегистрированы без принятия правил сервиса")
            return redirect('projects:list')
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
        payment, created = Payments.objects.get_or_create(
            rentor = request.user,
            renta_id = None,
            price = 1,
            date = timezone.now(),
            payment_type = 'P'
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
            "confirmation": {
                "type": "redirect",
                "return_url": "https://e064f267.ngrok.io/users/accounts/addcard/confirmation"
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
    else:

        return render(request, 'user/payment.html', {})

@login_required(login_url='/accounts/login/')
def UserAddCardConfirm(request):
    try:
        if request.user.usersdocuments.yakey is not None:
            return redirect('projects:list')
    except:
        return redirect('user:userDocuments')
    payment_obj = Payments.objects.filter(rentor=request.user,payment_type = 'P').last()
    payment = Payment.find_one(payment_obj.payment_id)
    if payment.status == 'waiting_for_capture':
        print(payment.payment_method.id)
        request.user.usersdocuments.yakey = payment.payment_method.id
        request.user.usersdocuments.save()
        payment.status
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
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('projects:list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
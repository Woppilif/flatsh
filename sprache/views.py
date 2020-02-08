from django.shortcuts import render , get_object_or_404, redirect
from django.http import HttpResponse
# Create your views here.
from yandex_checkout import Payment,Configuration
from django.conf import settings
from django.utils import timezone
import uuid
from sprache.models import UserAccount
from sprache.forms import UserDocumentsForm
import decimal
from django.core.mail import send_mail
Configuration.account_id = settings.YA_ACCOUNT_ID
Configuration.secret_key = settings.YA_SECRET_KEY


def index(request):
    if request.method == 'POST':
        form = UserDocumentsForm(data=request.POST)
        if form.is_valid():
            ud = form.save()
            ud.key = str(uuid.uuid4())
            ud.created_at = timezone.now()
            ud.save()
            return redirect('sprache:pay',payment_id=ud.key)
    else:
        form = UserDocumentsForm
    return render(request,"sprache/index.html",{"form":form})

def pay(request,payment_id):
    order = get_object_or_404(UserAccount,key = payment_id)
    payment = Payment.create({
        "amount": {
            "value": "{0}".format(str(decimal.Decimal(order.price))),
            "currency": "RUB"
        },

        "confirmation": {
            "type": "embedded"
        },
        "receipt": {
        "customer": {
            "full_name": "{0} {1}".format(order.first_name,order.last_name),
            "email": "{0}".format(order.email)
        },
        "items": [
                {
                    "description": "Оплата занятий",
                    "quantity": "2.00",
                    "amount": {
                        "value": "{0}".format(str(decimal.Decimal(order.price))),
                        "currency": "RUB"
                    },
                    "vat_code": "2",
                    "payment_mode": "full_prepayment",
                    "payment_subject": "commodity"
                }
            ]
        },
        "capture": True,
        "description": "Заказ №{0}".format(order.pk)
    })
    order.payment_id = payment.id
    order.save()
    return render(request,"sprache/pay.html",{"payment":payment,"order":order})

def paycheck(request,payment_id):
    order = get_object_or_404(UserAccount,key = payment_id)
    payment = Payment.find_one(order.payment_id)
    if payment.status == "succeeded":
        order.status = True
        order.save()
        try:
            send_mail(
                'Алгоритм языка | Оплата занятий',
                'Вы успешно оплатили заказ № {0} на сумму: {1}'.format(order.pk,str(decimal.Decimal(order.price))),
                'ewtm.info@gmail.com',
                ['{0}'.format(order.email)],
                fail_silently=False,
            )
        except Exception as e:
            print("Email sendr exception {0}".format(e))
    return render(request,"sprache/success.html",{"number":order.pk})



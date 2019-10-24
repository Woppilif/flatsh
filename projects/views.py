from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
import uuid
from sharing.models import Rents, Access, Payments, Flats, Images
from .forms import RentForm
import uuid
from yandex_checkout import Payment,Configuration 
from datetime import timedelta
from django.utils import timezone
from api.views import openDoorAPI
Configuration.account_id = 591310

Configuration.secret_key = "test_1J9BQa-AGyxrN3U9x7CrJ6l4bM0ri8L5a5aGcBj7T_w"
# Create your views here.


@login_required(login_url='/accounts/login/')
def projects(request):
    try:
        if request.user.usersdocuments.yakey is None:
            return redirect('user:UserAddCard')
    except:
        return redirect('user:UserAddCard')

    project_list = currentRentaDef(request.user)
    if project_list == '':
        flats = Flats.objects.filter(status='U')
    else:
        flats = Flats.objects.filter(id=project_list.flat.id)
    
    return render(request, 'projects/main.html', {'flats':flats,'project_list':project_list})

def currentRentaDef(user):
    ob = Rents.objects.filter(rentor=user,end__gt=timezone.now()).exclude(status__exact=None).last()
    if ob is not None:
        return ob
    return ''

@login_required(login_url='/accounts/login/')
def project_list(request,ltype):
    data = dict()
    project_list = currentRentaDef(request.user)
    if project_list == '':
        flats = Flats.objects.filter(status='U')
    else:
        flats = Flats.objects.filter(id=project_list.flat.id)
    if ltype == 1:
        template = 'projects/includes/partial_book_list.html'
    else:
        template = 'projects/flats/map.html'
    data['html_book_list'] = render_to_string(template, {
        'flats':flats
    })
  
    data['form_is_valid'] = True
    return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def project_flat(request,pk,ltype='map'):
    data = dict()
    flat = Flats.objects.get(pk=pk) #status__exact=None
    project_list = currentRentaDef(request.user)
    images = Images.objects.filter(flat=flat)
    data['html_book_list'] = render_to_string('projects/flats/flat.html', {
        'flat':flat,
        'back':ltype,
        'images':images,
        'project_list':project_list
    })
    data['form_is_valid'] = True
    return JsonResponse(data)

def currentRenta(request):
    project_list = currentRentaDef(request.user)
    return render(request, 'projects/rents.html', {'project_list':project_list})


def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            ff = form.save(commit=False)
            try:
                obj = Rents.renta.createRent(flat=form.current_flat,user=request.user,start=ff.start,end=ff.end)
                print(obj)
            except:
                obj = None
                print('Renta object wasnt created!')
            if obj is not None:
                if timezone.now().hour >= 15 and timezone.now() >= ff.start:
                    rentaStart(request,obj.pk)
                if request.user.usersdocuments.totlal_cancelation > 2:
                    request.user.usersdocuments.totlal_cancelation = 0
                    request.user.usersdocuments.save()
                    rentaStart(request,obj.pk)
            '''
            project = form.save(commit=False) #
            project.rentor = request.user
            project.flat = form.current_flat
            project.save()
            '''
            data['form_is_valid'] = True
            project_list = currentRentaDef(request.user)
            if project_list == '':
                flats = Flats.objects.filter(status='U')
            else:
                flats = Flats.objects.filter(id=project_list.flat.id)
            data['html_book_list'] = render_to_string('projects/flats/map.html', {
                'project_list':project_list, 'flats':flats
            })
            data['user_bar'] = render_to_string('projects/flats/rents_part.html', {
                'project_list':project_list
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    
    return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def project_create(request,pk):
    if currentRentaDef(request.user) != '':
        return redirect("projects:list")
    flat = get_object_or_404(Flats, pk=pk)
    if request.method == 'POST':
        form = RentForm(data=request.POST,current_flat=flat)
    else:
        form = RentForm(current_flat=flat)
    return save_book_form(request, form, 'projects/includes/partial_book_create.html')

@login_required(login_url='/accounts/login/')
def project_update(request, pk):
    book = get_object_or_404(Rents, pk=pk)
    if request.method == 'POST':
        form = RentForm(data=request.POST, instance=book)
    else:
        form = RentForm(instance=book)
    return save_book_form(request, form, 'projects/includes/partial_book_update.html')

@login_required(login_url='/accounts/login/')
def project_delete(request, pk):
    book = get_object_or_404(Rents, pk=pk)
    data = dict()
    if request.method == 'POST':
        #book.delete()
        book.status = None
        book.save()
        data['form_is_valid'] = True
        project_list = currentRentaDef(request.user)
        data['html_book_list'] = render_to_string('projects/includes/partial_book_list.html', {
            'project_list':project_list
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('projects/includes/partial_book_delete.html', context, request=request)
    return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def flatPay(request,pk):
    rentaStart(request,pk)
    return redirect('projects:list')

def rentaStart(request,pk):
    renta = get_object_or_404(Rents,rentor=request.user,status=True,id = pk,paid=False)

    deposit, created = Payments.objects.get_or_create(
        rentor = request.user,
        renta = renta,
        price = renta.flat.deposit,
        date = timezone.now(),
        payment_type = 'D'
    )

    depositPayment = Payment.create({
        "amount": {
            "value": renta.flat.deposit,
            "currency": "RUB"
        },
        "payment_method_id": request.user.usersdocuments.yakey,
        "description": "Заказ ID:{0} Оплата депозита".format(deposit.pk)
    })

    deposit.payment_id = depositPayment.id
    deposit.payment_status = depositPayment.status
    deposit.created_at = depositPayment.created_at
    deposit.expires_at = depositPayment.expires_at
    deposit.status = True
    deposit.save()

    full, created = Payments.objects.get_or_create(
        rentor = request.user,
        renta = renta,
        price = renta.getPrice(),
        date = timezone.now(),
        payment_type = 'F'
    )

    fullPayment = Payment.create({
        "amount": {
            "value": full.price,
            "currency": "RUB"
        },
        "payment_method_id": request.user.usersdocuments.yakey,
        "description": "Заказ ID:{0} Оплата аренды".format(deposit.pk)
    })
    idempotence_key = str(uuid.uuid4())
    response = Payment.capture(
        fullPayment.id,
        {
            "amount": {
            "value": full.price,
            "currency": "RUB"
            }
        },
        idempotence_key
    )
    print(response.status)
    if response.status == 'succeeded':
        fullPayment = Payment.find_one(response.id)
        full.payment_id = fullPayment.id
        full.payment_status = fullPayment.status
        full.created_at = fullPayment.created_at
        full.expires_at = fullPayment.expires_at
        full.status = True
        full.save()
        full.renta.paid = True
        full.renta.save()
        acc = Access.objects.create(
            user = request.user,
            renta = full.renta,
            start = full.renta.start,
            end = full.renta.end
        )
    request.user.usersdocuments.totlal_cancelation = 0
    request.user.usersdocuments.save()
    return True

@login_required(login_url='/accounts/login/')
def access(request):
    renta = Rents.objects.filter(rentor=request.user).exclude(status__exact=None).last()
    acc = renta.AccessObj() #get_object_or_404(Access, pk=pk,user=request.user)
    #print(acc.get_absolute_url())
    acc.setStartTime()
    if acc.CheckAccess():
        print("Signal sent to {0}".format(renta.flat.id))
        acc.usedAdd()
        openDoorAPI(renta.flat.id,renta.flat.app_id)
    else:
        print("Rights expired!")
    data = dict()
    project_list = currentRentaDef(request.user)
    data['html_book_list'] = render_to_string('projects/flats/rents_part.html', {
                'project_list':project_list
    })
    data['time'] = str("08:00")
    data['form_is_valid'] = True
    return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def rentCancel(request,pk):
    renta = get_object_or_404(Rents,rentor=request.user,status=True,id = pk,paid=False)
    
    if timezone.now().hour >= 15:
        return redirect('projects:flatPay',pk=renta.pk)
    else:
        renta.status = None
        renta.save()   
        request.user.usersdocuments.totlal_cancelation = request.user.usersdocuments.totlal_cancelation + 1
        request.user.usersdocuments.save()
    return redirect('projects:list')


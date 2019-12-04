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
from api.tasks import start_renta_task
# Create your views here.

def trial_renta(request, trial_key):
    flats = get_object_or_404(Rents,trial_key=trial_key,status=True,paid=True)
    flats = [flats]
    return render(request, 'projects/trial.html', {'flats':flats})



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
    ob = Rents.objects.filter(rentor=user,end__gt=timezone.now()).exclude(status__exact=None).first()
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
                access = Access.access.createAccess(obj)
                print("Renta created {0}".format(obj))
                print("And access {0}".format(access))
            except:
                obj = None
                print('Renta object wasnt created!')
           
            if obj is not None:
                '''
                if timezone.now().hour >= 15 and timezone.now() >= ff.start:
                    rentaStart(request.user,obj.pk)
                '''
                if request.user.usersdocuments.totlal_cancelation > 2:
                    request.user.usersdocuments.totlal_cancelation = 0
                    request.user.usersdocuments.save()
                    rentaStart(request.user,obj.pk)
          

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
    renta = get_object_or_404(Rents,rentor=request.user,status=True,id = pk,paid=False)
    deposit = Payments.paym.createPayment(renta=renta,p_type=1)
    print("Renta deposit obj created {0}".format(deposit))
    full = Payments.paym.createPayment(renta=renta,p_type=2)
    print("Renta payment obj created {0}".format(full))
    access = Access.access.createPaidAccess(full.renta)
    print("And access {0}".format(access))
    return redirect('projects:list')

def rentaStart(user,pk):
    return True

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
    if timezone.now() >= renta.booking:
        return redirect('projects:flatPay',pk=renta.pk)
    else:
        renta.status = None
        renta.save()   
        request.user.usersdocuments.totlal_cancelation = request.user.usersdocuments.totlal_cancelation + 1
        request.user.usersdocuments.save()
    return redirect('projects:list')

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
    data = dict()
    data['html_book_list'] = render_to_string('projects/flats/trial.html', {
                'flats':[renta]
    })
    data['form_is_valid'] = True
    return JsonResponse(data)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from sharing.models import Rents, Flats, Images, UsersDocuments, Payments, Access
from sharing.forms import FlatEditForm, FlatImagesForm
from django.contrib import messages
from django.contrib.auth.models import User
import uuid
from sharing.forms import RentFormEx

def checkRoleManager(function):
    '''
        Redirect user to booked object if he has one
    '''
    def decorator(request, *args, **kwargs):
        try:
            role = request.user.workers.role
        except:
            return redirect('rents:map')
        if role != 1:
            return redirect('rents:map')
        return function(request, *args, **kwargs)
    return decorator

@login_required(login_url='/accounts/login/')
@checkRoleManager
def index(request):
    rents = Rents.objects.filter(trial_key__isnull=False,status=True).order_by('-start')
    return render(request,"trial/index.html",{"rents":rents})
    
@login_required(login_url='/accounts/login/')
@checkRoleManager
def save_trial_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            ff = form.save(commit=False) #
            flat =  Flats.objects.get(pk=int(request.POST.get("flat")))
            obj = Rents.renta.createRent(flat=flat,user=request.user,start=ff.start,end=ff.end)
            obj.status = True
            obj.paid = ff.paid
            obj.trial_key = str(uuid.uuid4())
            obj.save()
            access = Access.access.createPaidAccess(obj)
            print("Renta created {0}".format(obj))
            print("And access {0}".format(access))
            
            data['form_is_valid'] = True
            rents = Rents.objects.filter(trial_key__isnull=False,status=True).order_by('-start')
            data['html_book_list'] = render_to_string('trial/includes/partial_book_list.html', {
                'rents':rents, 'new':obj.pk
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def trial_create(request):
    if request.method == 'POST':
        form = RentFormEx(data=request.POST)
    else:
        form = RentFormEx()
    return save_trial_form(request, form, 'trial/includes/partial_book_create.html')

'''
@login_required(login_url='/accounts/login/')
def managers(request):
    print(request.user.workers.account)
    flats = Flats.objects.filter(district__partner=request.user.workers.partner)
    manager_list = Rents.objects.filter(status=True)
    return render(request, 'calendar/manager_list2.html', {'manager_list':manager_list,'flats':flats})

@login_required(login_url='/accounts/login/')
def users(request,pk = None):
    users = get_object_or_404(User, pk=pk)
    last = Rents.objects.filter(rentor=users).last()
    if last is None:
        return redirect('sharing:flats')
    print(last.flat.district.partner,request.user.workers.partner)
    if last.flat.district.partner != request.user.workers.partner:
        return redirect('sharing:flats')
    rents = Rents.objects.filter(rentor=users,flat__district__partner=request.user.workers.partner)
    payments = Payments.objects.filter(rentor=users,renta__in=[i.pk for i in rents])
    return render(request, 'users/users_list.html', {'users':users,'rents':rents,'payments':payments})

@login_required(login_url='/accounts/login/')
def blockUser(request,pk = None):
    users = get_object_or_404(User, pk=pk)
    last = Rents.objects.filter(rentor=users).last()
    if last is not None:
        if last.flat.district.partner != request.user.workers.partner:
            return redirect('flats:flats')
    if users.is_active == False:
        users.is_active = True
    else:
        users.is_active = False
    users.save()
    return redirect('sharing:users',pk=pk)





@login_required(login_url='/accounts/login/')
def flats(request):
    if checkRoleManager(request):
        return checkRoleManager(request)
    print(request.user.workers.role)
    flats = Flats.objects.filter(district__partner_id=request.user.workers.partner.id)
    print(flats)
    return render(request, 'managers/manager_list.html', {'flats':flats})

@login_required(login_url='/accounts/login/')
def flatsEdit(request,pk):
    flats = get_object_or_404(Flats, pk=pk,district__partner=request.user.workers.partner)
    images = Images.objects.filter(flat=flats)
    rents = Rents.objects.filter(flat=flats)
    if checkRoleManager(request):
        return checkRoleManager(request)
    form = FlatEditForm(data=request.POST, instance=flats,current_user=request.user)
    form_images = FlatImagesForm(files=request.FILES,data=request.POST)
    if request.method == 'POST' and 'flat_save' in request.POST:
        print("NOT IMG")
        if form.is_valid():
            manager = form.save(commit=False) #
            manager.creator = request.user
            manager.save()
            messages.success(request,"Данные успешно обновлены!")
            return redirect("sharing:flatsEdit",pk=flats.pk)
    if request.method == 'POST' and 'image_save' in request.POST:
        if form_images.is_valid():
            manager = form_images.save(commit=False) #
            manager.flat = flats
            manager.save()
            messages.success(request,"Изображение добавлено!")
            return redirect("sharing:flatsEdit",pk=flats.pk)

    else:
        form_images = FlatImagesForm(current_user=request.user, instance=flats)
        form = FlatEditForm(instance=flats,current_user=request.user)
    return render(request, 'managers/flats/flat.html', {'flats':flats,'form':form,'images':images,'rents':rents,'form_images':form_images})

def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            manager = form.save(commit=False) #
            manager.creator = request.user

            manager.save()
            
            data['form_is_valid'] = True
            manager_list = Rents.objects.filter()
            data['html_book_list'] = render_to_string('managers/includes/partial_book_list.html', {
                'manager_list':manager_list
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def manager_create(request):
    
    if request.method == 'POST':
        form = FlatEditForm(data=request.POST,current_user=request.user)
    else:
        form = FlatEditForm(current_user=request.user)
    return save_book_form(request, form, 'managers/includes/partial_book_create.html')


def manager_update(request, pk):
    book = get_object_or_404(Flats, pk=pk,district__partner=request.user.workers.partner)
    if request.method == 'POST':
        form = FlatEditForm(data=request.POST, instance=book,current_user=request.user)
    else:
        form = FlatEditForm(instance=book,current_user=request.user)
    return save_book_form(request, form, 'managers/includes/partial_book_update.html')


def manager_delete(request, pk):
    book = get_object_or_404(Rents, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True
        manager_list = Rents.objects.filter()
        data['html_book_list'] = render_to_string('managers/includes/partial_book_list.html', {
            'manager_list':manager_list
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('managers/includes/partial_book_delete.html', context, request=request)
    return JsonResponse(data)
'''


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Rents, Flats, Images
from .forms import FlatEditForm, FlatImagesForm
from django.contrib import messages

def index(request):
    if request.user.is_authenticated:
        return redirect("projects:list")
    return render(request,"home.html")

@login_required(login_url='/accounts/login/')
def managers(request):
    print(request.user.workers.account)
    flats = Flats.objects.filter(district__partner=request.user.workers.partner)
    manager_list = Rents.objects.filter(status=True)
    return render(request, 'calendar/manager_list.html', {'manager_list':manager_list,'flats':flats})

def checkRoleManager(request):
    if request.user.workers.role != 1:
        return redirect('projects:list')
    return False


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

'''
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


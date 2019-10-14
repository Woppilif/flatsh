from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Rents, Flats
from .forms import RentForm

def index(request):
    if request.user.is_authenticated:
        return redirect("projects:list")
    return render(request,"home.html")

@login_required(login_url='/accounts/login/')
def managers(request):
    flats = Flats.objects.all()
    manager_list = Rents.objects.filter(status=True)
    return render(request, 'managers/manager_list.html', {'manager_list':manager_list,'flats':flats})


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
def manager_refresh(request):
    data = dict()
    manager_list = Rents.objects.filter()
    data['html_book_list'] = render_to_string('managers/includes/partial_book_list.html', {
                'manager_list':manager_list
    })
  
    data['form_is_valid'] = True
    return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def manager_create(request):
    
    if request.method == 'POST':
        form = RentForm(data=request.POST,current_user=request.user)
    else:
        form = RentForm(current_user=request.user)
    return save_book_form(request, form, 'managers/includes/partial_book_create.html')


def manager_update(request, pk):
    book = get_object_or_404(Rents, pk=pk)
    if request.method == 'POST':
        form = RentForm(data=request.POST, instance=book,current_user=request.user)
    else:
        form = RentForm(instance=book,current_user=request.user)
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


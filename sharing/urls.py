from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'sharing'

urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.managers, name='managers'),
    path('flats/', views.flats, name='flats'),
    path('flats/<int:pk>/change', views.flatsEdit, name='flatsEdit'),
    path('create/', views.manager_create, name='manager_create'),
    path('update/<int:pk>', views.manager_update, name='manager_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

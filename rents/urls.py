from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rents import views

app_name = 'rents'

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registration, name='registration'),
    path('map/', views.map, name='map'),
    path('act/<int:pk>', views.act, name='act'),
    #path('act/<int:pk>/pay', views.actpay, name='actpay'),
    path('apartment/<int:pk>', views.apartment, name='apartment'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/<int:pk>', views.favoritesAdd, name='favoritesAdd'),
    path('list/', views.lists, name='list'),
    path('opendoor/<int:pk>', views.opendoor, name='opendoor'),
    #path('openpay/<int:pk>', views.openpay, name='openpay'),
    path('options/', views.options, name='options'),
    path('card/', views.card, name='card_oper'),
    path('card/<uuid:code>', views.card, name='card'),
    path('bot/', views.bot, name='bot'),
    path('access/', views.access, name='access'),
    path('trial/<uuid:trial_key>/pay', views.trial_pay, name='trial_pay'),
    path('trial/<uuid:trial_key>', views.trial_renta, name='trial_renta'),
    path('trial_open/<uuid:trial_key>', views.trial_access, name='trial_access'),
    path('file/', views.upload_file, name='upload_file'),
    path('rules/', views.user_agreement, name='user_agreement'),
    path('agreement/', views.agreement, name='agreement'),
    path('device/<uuid:dkey>', views.device, name='device'),
    path('bitx/', views.bitx_data, name='bitx_data'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
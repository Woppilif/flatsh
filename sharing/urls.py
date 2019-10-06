from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'sharing'

urlpatterns = [
    path('', views.index, name='index'),
    
    #path('flats/', views.loadFlats, name='flats'),
    path('pay/<int:pk>/deposit', views.flatPayDeposit, name='flatPayDeposit'),
    path('pay/<int:pk>/renta', views.flatPayRenta, name='flatPayRenta'),
    path('pay/', views.addCard, name='addCard'),
    path('pay2/', views.addCard2, name='addCard2'),
    path('pay/order/<int:pk>', views.OnPaymentCallback, name='OnPaymentCallback'),

    path('access/<int:pk>', views.access, name='access'),
    path('cancel/<int:pk>', views.rentCancel, name='rentCancel'),
    path('test/', views.test, name='test'),

    #path('user/', views.UserPage, name='user'),
    #path('accounts/register', views.UserRegister, name='userRegister'),
    #path('user/documents', views.UserDocuments, name='userDocuments'),

    path('flat/<int:pk>', views.flatInfo, name='flatInfo'),
    path('flat/<int:pk>/start', views.startRent, name='startRent'),
    path('flats/', views.flatsFilter, name='flats_filter'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#2521c2e3-000f-5000-a000-15bb9a95a0f4
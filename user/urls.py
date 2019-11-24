from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'user'

urlpatterns = [
    path('accounts/register', views.UserRegister, name='userRegister'),
    path('accounts/documents', views.UserDocuments, name='userDocuments'),
    path('accounts/addcard', views.UserAddCard, name='UserAddCard'),
    path('accounts/addcard/confirmation', views.UserAddCardConfirm, name='UserAddCardConfirm'),
    path('accounts/settings', views.UserSettingsMenu, name='settings'),
    path('accounts/deletecard', views.deletecard, name='deletecard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

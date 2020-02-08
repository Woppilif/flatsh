from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from sprache import views

app_name = 'sprache'

urlpatterns = [
    path('', views.index, name='index'),
    path('pay/<uuid:payment_id>', views.pay, name='pay'),
    path('pay/<uuid:payment_id>/check', views.paycheck, name='paycheck'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
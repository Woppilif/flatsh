from django.urls import path, re_path

from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.projects, name='list'),
    path('create/<int:pk>', views.project_create, name='project_create'),
    path('update/<int:pk>', views.project_update, name='project_update'),
    path('delete/<int:pk>', views.project_delete, name='project_delete'),
    path('list/<int:ltype>', views.project_list, name='project_list'),
    path('flat/<int:pk>/<int:ltype>', views.project_flat, name='project_flat'),
    path('renta/', views.currentRenta, name='currentRenta'),

    path('pay/<int:pk>', views.flatPay, name='flatPay'),
    #path('pay/<int:pk>/<str:ptype>', views.flatPay, name='flatPayRenta'),
    #path('pay/order/<int:pk>', views.OnPaymentCallback, name='OnPaymentCallback'),

    path('access/', views.access, name='access'),
    path('cancel/<int:pk>', views.rentCancel, name='rentCancel'),


]
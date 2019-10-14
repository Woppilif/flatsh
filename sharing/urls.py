from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'sharing'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.managers, name='managers'),
    path('create/', views.manager_create, name='manager_create'),
    path('update/<int:pk>', views.manager_update, name='manager_update'),
    path('delete/<int:pk>', views.manager_delete, name='manager_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#2521c2e3-000f-5000-a000-15bb9a95a0f4
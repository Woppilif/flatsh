from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import manager

app_name = 'sharing'

urlpatterns = [
    path('', manager.index, name='index'),
    path('create/', manager.trial_create, name='trial_create'),
]
'''
path('calendar/', views.managers, name='managers'),
path('flats/', views.flats, name='flats'),
path('users/<int:pk>', views.users, name='users'),
path('users/<int:pk>/block', views.blockUser, name='blockUser'),
path('flats/<int:pk>/change', views.flatsEdit, name='flatsEdit'),

path('update/<int:pk>', views.manager_update, name='manager_update'),
'''
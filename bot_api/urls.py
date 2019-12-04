from django.urls import path, re_path

from . import views

app_name = 'bot_api'

urlpatterns = [
    path('update/', views.bot_api_update, name='bot_api_update'),
    path('telegram/', views.telegram, name='telegram'),
]
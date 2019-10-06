from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('1/<int:pk>', views.index, name='index'),
    path('2/<int:pk>', views.index2, name='index2'),
    path('3/<str:group_name>', views.index3, name='index2'),
] 
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mentor_list, name='mentor_list'),
    path('create/', views.mentor_fields_create, name='mentor_fields_create')
]

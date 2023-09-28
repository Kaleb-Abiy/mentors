from django.urls import path
from . import views

urlpatterns = [
    path('', views.mentor_list, name='mentor_list'),
    path('<int:id>', views.mentor_detail, name='mentor_detail'),
    path('create/', views.mentor_fields_create, name='mentor_fields_create'),
    path('show/', views.show, name='show')
]

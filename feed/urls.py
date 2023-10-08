from django.urls import path
from . import views

urlpatterns = [
    path('', views.mentor_list, name='mentor_list'),
    path('<int:id>', views.mentor_detail, name='mentor_detail'),
    path('create/', views.mentor_fields_create, name='mentor_fields_create'),
    path('set_availability/', views.set_availability, name='set_availability'),
    path('show/', views.show, name='show'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('verify/', views.verify_payment, name='verify_payment'),
]

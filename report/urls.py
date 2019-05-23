from django.contrib import admin
from django.urls import path

from . import views

app_name = 'report'
urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard_creator', views.dashboard_creator, name='dashboard_creator'),
    path('create', views.create, name='create'),
    path('documents', views.documents, name='documents'),
    path('erase/<page_slug>', views.erase, name='erase'),
    path('<page_slug>/input', views.input, name='input'),
    path('<page_slug>/submissions/<int:pk>', views.edit, name='edit'),
    path('<page_slug>/submissions', views.submissions, name='submissions'),
    path('<page_slug>/approval', views.approval, name='approval'),
    path('<page_slug>/delete', views.delete, name='delete'),
    path('<page_slug>/deletion/<int:pk>', views.deletion, name='deletion'),
    path('profile', views.profile, name='profile'),
    path('completed', views.completed, name='completed'),
]

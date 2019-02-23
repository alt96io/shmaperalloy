from django.urls import path

from . import views

app_name = 'report'
urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('input', views.input, name='input'),
    path('edit/<int:taskname_id>', views.edit, name='edit'),
    path('submissions', views.submissions, name='submissions'),
    path('completed', views.completed, name='completed'),
]

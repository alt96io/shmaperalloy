from django.urls import path

from . import views

app_name = 'report'
urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('input', views.input, name='input'),
    path('submissions/<int:pk>', views.edit, name='edit'),
    path('submissions', views.submissions, name='submissions'),
    path('deletion/<int:pk>', views.deletion, name='deletion'),
    path('completed', views.completed, name='completed'),
]


from django.urls import include, path

urlpatterns = [
    path('report/', include('report.urls')),
]

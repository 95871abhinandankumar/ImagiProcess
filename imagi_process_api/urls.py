from django.urls import path
from .views import upload_csv, check_request_status

urlpatterns = [
    path('upload_csv/', upload_csv, name='upload_csv'),
    path('check_request_status/<str:request_id>/', check_request_status, name='check_request_status'),
]
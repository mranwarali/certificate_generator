from django.urls import path, include
from certificates.views import create_certificate, view_certificate, verify_certificate

urlpatterns = [
    path('', create_certificate, name='create_certificate'),
    path('verify/', verify_certificate, name='verify_certificate'),
    path('view/<int:certificate_id>/', view_certificate, name='view_certificate'),
]

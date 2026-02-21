from django.http import JsonResponse
from django.urls import path, include


def health(request):
    return JsonResponse({
        "status": "ok",
        "message": "HRMS Backend API",
    })


api_patterns = [
    path('health/', health, name='health'),
    path('employees/', include('employees.urls')),
    path('attendance/', include('attendance.urls')),
]

urlpatterns = [
    path('', health, name='root'),
    path('api/', include(api_patterns)),
]

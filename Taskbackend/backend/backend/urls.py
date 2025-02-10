from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # Includes accounts URLs
    path('api/tasks/', include('tasks.urls')),        # Includes tasks URLs
]

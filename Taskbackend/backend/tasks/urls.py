from django.urls import path
from .views import addtask, List, delete

urlpatterns = [
    path('addtask/', addtask, name='addtask'),  # Added trailing slash
    path('list/', List, name='list'),          # Added trailing slash
    path('delete/<int:pk>/', delete, name='delete'),

]

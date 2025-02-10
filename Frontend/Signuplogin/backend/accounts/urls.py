from django.urls import path
from .views import signup, login, forgot_password, reset_password

urlpatterns = [
    path('signup/', signup, name='signup'),  # Added trailing slash
    path('login/', login, name='login'), 
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('reset-password/<int:user_id>/<str:token>/', reset_password, name='reset-password'),   # Added trailing slash
]

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import UserLoginForm

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html',
                                                authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.update_profile, name='update_profile'),
    path('verify/<email>/<token>', views.verify, name='verify'),
]

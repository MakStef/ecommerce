from django.urls import path
from .views import (
    SettingsView,
    RegisterView,
    LoginView,
    logoutView,
    ChangeView,
    ForgotPasswordView,
)
app_name = 'accounts'

urlpatterns = [
    path('', SettingsView.as_view(), name='settings'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logoutView, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('changepassword/', ChangeView.change_password, name='change_password'),
    path('changeemail/', ChangeView.change_email, name='change_email'),
    path('delete/', ChangeView.delete, name='delete'),
    path('forgot_password/', ForgotPasswordView.as_view(), name="forgot_password"),
]

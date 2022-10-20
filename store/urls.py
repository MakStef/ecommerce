from django.urls import path
from .views import (
    HomepageView,
    NewslettersView,
)
app_name = 'store'

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('newsletters/', NewslettersView.as_view(), name='newsletter'),
]

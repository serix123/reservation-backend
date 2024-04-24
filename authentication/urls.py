from django.urls import path, include
from .views import user_views

urlpatterns = [
    path("register/", user_views.register, name="user-registration" ),
]
from django.urls import path
from .views import registration_endpoint
# Copyright Videntity Systems, Inc

urlpatterns = [
    path('register', registration_endpoint, name="registration_endpoint"),

]

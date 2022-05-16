from django.urls import path
from .views import SignUpAPI
urlpatterns = [

    #API
    path('sign_up_API/', SignUpAPI.as_view())
]
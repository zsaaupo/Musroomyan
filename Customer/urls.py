from django.urls import path
from .views import SignUpAPI, OTPCheckingAPI
urlpatterns = [

    #API
    path('sign_up_API/', SignUpAPI.as_view()),
    path('OTP_checking/', OTPCheckingAPI.as_view()),
]
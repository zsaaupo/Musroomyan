from django.urls import path
from .views import SignUpAPI, OTPCheckingAPI, SignInAPI, sing_up
urlpatterns = [

    path('sign_up/', sing_up),

    #API
    path('sign_up_API/', SignUpAPI.as_view()),
    path('OTP_checking/', OTPCheckingAPI.as_view()),
    path('sign_in_API/', SignInAPI.as_view()),
]
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from .models import CustomerData

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import random

class SignUpAPI(CreateAPIView):
    permission_classes = []
    def post(self, request):
        result = {}

        try:
            #tring to get user data
            data = request.data
            if 'full_name' not in data or data['full_name'] == '':
                result['massage'] = "Name can not be null."
                result['error'] = "Full name"
                return Response(result, status= HTTP_400_BAD_REQUEST)
            if 'email' not in data or data['email'] == '':
                result['massage'] = "Email can not be null."
                result['error'] = "Email"
                return Response(result, status=HTTP_400_BAD_REQUEST)
            if 'phone_number' not in data or data['phone_number'] == '':
                result['massage'] = "Phone number can not be null."
                result['error'] = "Phone number"
                return Response(result, status=HTTP_400_BAD_REQUEST)
            if 'address' not in data or data['address'] == '':
                result['massage'] = "Address number can not be null."
                result['error'] = "Address"
                return Response(result, status=HTTP_400_BAD_REQUEST)
            if 'gender' not in data or data['gender'] == '':
                result['massage'] = "Gender number can not be null."
                result['error'] = "Gender"
                return Response(result, status=HTTP_400_BAD_REQUEST)
            if 'password' not in data or data['password'] == '':
                result['massage'] = "Password number can not be null."
                result['error'] = "Password"
                return Response(result, status=HTTP_400_BAD_REQUEST)

            user = User.objects.filter(username=data['email']).first() #filtering user

            if user:
                return Response("You already have an account")

            if not user:
                user = User()
                user.username = data['email']
                user.first_name = data['full_name']
                user.email = data['email']
                user.password = make_password(data['password'])
                user.is_active = False
                user.save()
                # user saved

                OTP_maker = random.randint(777, 7777)

                customer = CustomerData()
                customer.full_name = data['full_name']
                customer.email = data['email']
                customer.phone_number = data['phone_number']
                customer.address = data['address']
                customer.gender = data['gender']
                customer.OTP = OTP_maker
                customer.user = user
                customer.save()
                # new customer saved

                result['status'] = HTTP_200_OK
                result['massage'] = "Success"
                result['email'] = data['email']
                return Response(result)
        except Exception as ex:
            return Response(str(ex))
        return Response("True")
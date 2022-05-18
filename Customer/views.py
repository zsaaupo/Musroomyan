import json
from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_203_NON_AUTHORITATIVE_INFORMATION, HTTP_226_IM_USED, HTTP_202_ACCEPTED, HTTP_406_NOT_ACCEPTABLE, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY,

from .models import CustomerData

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
import random

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from threading import Thread


def OTP_sender(to, subject, body):
    sender_email = 'django2077@gmail.com'

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', '465')
        server.ehlo()
        server.login(sender_email, '2077dj007')

        massage = MIMEMultipart()
        massage['From'] = sender_email
        massage['To'] = to
        massage['Subject'] = subject

        html = """
        <html>
            <head></head>
            <body>
            <div>
                <h2>Welcome to Mushroomyan</h2>
                <h4>Thanks for Sign Up...!</h4>
                <h4>We can ensure that you can find best quality mushroom from us</h4>
            </div>
        """
        html += body
        """
            </body>
        </html>
        """

        massage.attach(MIMEText(html, 'html'))
        server.sendmail(
            from_addr=sender_email,
            to_addrs=to,
            msg=massage.as_string()
        )
        print("OTP sent")
    except Exception as ex:
        print(str(ex))
    finally:
        if server != None:
            server.quit()


def OTP_sender_thread(to, subject, body):
    Thread(target=OTP_sender, args=(to, subject, body)).start()


class SignUpAPI(CreateAPIView):
    permission_classes = []

    def post(self, request):
        result = {}
        try:
            # trying to get user data
            data = request.data  # form data variable
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
                result['massage'] = "Address can not be null."
                result['error'] = "Address"
                return Response(result, status=HTTP_400_BAD_REQUEST)
            if 'gender' not in data or data['gender'] == '':
                result['massage'] = "Gender can not be null."
                result['error'] = "Gender"
                return Response(result, status=HTTP_400_BAD_REQUEST)
            if 'password' not in data or data['password'] == '':
                result['massage'] = "Password can not be null."
                result['error'] = "Password"
                return Response(result, status=HTTP_400_BAD_REQUEST)

            user = User.objects.filter(username=data['email']).first()  # filtering user

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
                OTP_sender_thread(data['email'], 'Mushroomyan OTP', 'OTP : '+str(OTP_maker))
                # new customer saved

                result['status'] = HTTP_201_CREATED
                result['massage'] = "Success"
                result['email'] = data['email']
                return Response(result)
        except Exception as ex:
            return Response(str(ex))
        return Response("True")


class OTPCheckingAPI(CreateAPIView):
    permission_classes = []

    def put(self, request):
        result = {}
        try:
            data = json.loads(request.body)  # load json body as data
            if 'email' not in data or data['email'] == '':
                result['massage'] = "Email can not be null."
                result['error'] = "Email"
                return Response(result, status=HTTP_400_BAD_REQUEST)
            if 'OTP' not in data or data['OTP'] == '':
                result['massage'] = "OTP can not be null."
                result['error'] = "OTP"
                return Response(result, status=HTTP_400_BAD_REQUEST)

            user = User.objects.filter(username=data['email']).first()

            if not user:
                result['massage'] = "Please create an account"
                return Response(result, status=HTTP_203_NON_AUTHORITATIVE_INFORMATION)

            elif user.is_active:
                result['massage'] = "You have already have an active account"
                return Response(result, status=HTTP_226_IM_USED)

            else:
                customer = CustomerData.objects.filter(user=user).first()

                if customer.OTP == data['OTP']:
                    user.is_active = True
                    user.save()
                    customer.OTP = ''
                    customer.save()
                    result['massage'] = "Success."
                    result['status'] = HTTP_202_ACCEPTED
                    return Response(result)

                else:
                    result['status'] = HTTP_406_NOT_ACCEPTABLE
                    result['massage'] = " OTP did not matched."
                    result['error'] = "OTP"
                    return Response(result)

        except Exception as ex:
            return Response(str(ex))


class SignInAPI(CreateAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        result = {}

        try:
            data = json.loads(request.body)
            if 'email' not in data or data['email'] == '':
                result['massage'] = "Email can not be null."
                result['error'] = "Email"
                return Response(result, status=HTTP_400_BAD_REQUEST)
            if 'password' not in data or data['password'] == '':
                result['massage'] = "password can not be null."
                result['error'] = "password"
                return Response(result, status=HTTP_400_BAD_REQUEST)

            user = User.objects.filter(username=data['email']).first()

            if not user:
                result['massage'] = "Please create an account first"
                return Response(result, status=HTTP_203_NON_AUTHORITATIVE_INFORMATION)

            # under development
            elif not user.is_active:
                result['massage'] = "Your account is not active please contact our helpline"
                return Response(result, status=HTTP_422_UNPROCESSABLE_ENTITY)

            else:
                if not check_password(data['password'], user.password):
                    result['massage'] = "Wrong password"
                    return Response(result, status=HTTP_401_UNAUTHORIZED)

        except Exception as ex:
            return Response(str(ex))
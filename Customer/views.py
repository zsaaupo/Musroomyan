from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from .models import CustomerData

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
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
                OTP_sender_thread(data['email'], 'Mushroomyan OTP', 'OTP : '+str(OTP_maker))
                # new customer saved

                result['status'] = HTTP_200_OK
                result['massage'] = "Success"
                result['email'] = data['email']
                return Response(result)
        except Exception as ex:
            return Response(str(ex))
        return Response("True")
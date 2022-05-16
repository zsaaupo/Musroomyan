from django.db import models
from phonenumber_field.modelfields import PhoneNumberField, PhoneNumberDescriptor
from .string import gender_choice
from django.contrib.auth.models import User

class CustomerData(models.Model):

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = PhoneNumberField()
    address = models.TextField()
    gender = models.CharField(max_length=6, choices=gender_choice)
    OTP = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.full_name+" "+"("+str(self.phone_number)+")"

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class CustomerData(models.Model):

    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = PhoneNumberField()

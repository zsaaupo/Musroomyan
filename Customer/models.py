from django.db import models
from phonenumber_field.modelfields import PhoneNumberField, PhoneNumberDescriptor
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class CustomerData(models.Model):

    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = PhoneNumberField()
    address = models.TextField()

    def __str__(self):
        return self.full_name+" "+"("+str(self.phone_number)+")"

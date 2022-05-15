from django.contrib import admin
from .models import CustomerData

class CustomerDataAdmin(admin.ModelAdmin):

    list_display = [

    ]
admin.site.register(CustomerData, CustomerDataAdmin)

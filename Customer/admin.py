from django.contrib import admin
from .models import CustomerData

class CustomerDataAdmin(admin.ModelAdmin):

    list_display = [
        "full_name",
        "phone_number",
        "email",
    ]
admin.site.register(CustomerData, CustomerDataAdmin)

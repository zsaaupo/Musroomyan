from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("Stock.urls")),  # root html is stock.urls
    path('customer/', include("Customer.urls")),
    path('admin/', admin.site.urls),
]

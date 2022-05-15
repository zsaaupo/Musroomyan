from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("Stock.urls")),  # root html is stock.urls
    path('admin/', admin.site.urls),
]

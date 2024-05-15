from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Passenger

admin.site.register(Passenger, UserAdmin)

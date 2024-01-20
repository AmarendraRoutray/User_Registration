from django.contrib import admin

# Register your models here.
from .models import Profile

# admin.site.register(Profile)

@admin.register(Profile)
class ProfileAdminView(admin.ModelAdmin):
    list_display = ['username','address','profile_pic']
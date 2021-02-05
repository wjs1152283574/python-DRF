from django.contrib import admin
from .models import User,Departments
from django.contrib.auth.models import Permission,Group
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "username",
        "icon",
        "sex",
        "age",
        "mobile",
        "password",
        "last_login",
        "is_staff",
        "is_active",
        "is_superuser",
        "date_joined",
        "email",
    ]

# @admin.register(Group)
# class BMS_GroupAdmin(admin.ModelAdmin):
#     list_display = [
#         'pk',
#         'name'
#     ]

# @admin.register(Permission)
# class Bms_PermissionAdmin(admin.ModelAdmin):
#     list_display = [
#         'pk',
#         'name',
#         'content_type_id',
#         'codename'
#     ]

@admin.register(Departments)
class Bms_Departments(admin.ModelAdmin):
    list_display = [
        'pk',
        'depar_name',
        'depar_type'
    ]
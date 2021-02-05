from django.contrib import admin
from .models import BaseNav,Icons,SecondNav,ThirtNav
# Register your models here.

@admin.register(BaseNav)
class BaseNavAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'nav_name',
        'nav_icon',
        'add_time',
        'add_user'
    ]
@admin.register(Icons)
class IconsAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'icon',
        'icon_belong'
    ]
@admin.register(SecondNav)
class SecondNavAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'snav_name',
        'parannav',
        'snav_icon',
        'sadd_time',
        'sadd_user'
    ]
@admin.register(ThirtNav)
class ThirtNavAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'tnav_name',
        'parannav',
        'tnav_icon',
        'tadd_time',
        'tadd_user'
    ]
from rest_framework import serializers
from .models import BaseNav,Icons,SecondNav,ThirtNav

class IconsForBaseNav(serializers.ModelSerializer):
    class Meta:
        model = Icons
        fields = ['pk','icon']
        # read_only_fields = ["pk",'icon']

class BaseNavSerializers_post(serializers.ModelSerializer):
    # nav_icon = IconsForBaseNav()
    class Meta:
        model = BaseNav
        fields = [
            "pk",
            "nav_name",
            "nav_icon",
            "add_time",
            "add_user"
        ]
        read_only_fields = ["id", "add_time", "add_user"]

class BaseNavSerializers_get(serializers.ModelSerializer):
    nav_icon = IconsForBaseNav()
    class Meta:
        model = BaseNav
        fields = [
            "pk",
            "nav_name",
            "nav_icon",
            "add_time",
            "add_user"
        ]
        read_only_fields = ["id", "add_time", "add_user"]

class IconsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Icons
        fields = [
            "pk",
            "icon",
            "icon_belong"
        ]
        read_only_fields = ["pk","icon_belong"]

class SecondNavSerializers(serializers.ModelSerializer):
    class Meta:
        model = SecondNav
        fields = [
            "pk",
            "snav_name",
            "parannav",
            "sadd_time",
            "sadd_user",
            "snav_icon",
            "icon_name"
        ]
        read_only_fields = ["pk", "sadd_time", "sadd_user","icon_name"]

class ThirtNavSerializers(serializers.ModelSerializer):
    class Meta:
        model = ThirtNav
        fields = [
            "pk",
            "tnav_name",
            "parannav",
            "tnav_icon",
            "tadd_time",
            "tadd_user",
            "icon_name"
        ]
        read_only_fields = ["id", "tadd_time", "tadd_user","icon_name"]


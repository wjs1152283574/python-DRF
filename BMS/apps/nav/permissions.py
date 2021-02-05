from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group,Permission

# 管理员分组专有权限
class CheckAdmin(BasePermission):
    # 重写 权限验证方法
    def has_permission(self,request,view):
        if request.method == 'GET':
            return True
        else:
            group = Group.objects.filter(name='管理员').first()
            return bool(group in request.user.groups.all())   #　返回布尔值

# 特殊权限--超越分组
class SipecalPermissions(BasePermission):
    def has_permission(self,request,view):
        if request.method == 'GET':
            return True
        else:
            group = Group.objects.filter(name='管理员').first()
            return bool(group in request.user.groups.all())   #　返回布尔值
from rest_framework.permissions import BasePermission
from .models import UserAvatar,BlackUser
from django.contrib.auth.models import Group,Permission

# 用户只能删除自己的头像,不能随意删除其他用户的头像
class AvatarPermission(BasePermission):
    def has_permission(self,request,view):
        if request.method == "DELETE":
            user_avatar = UserAvatar.objects.filter(user=request.user).values_list()
            alls = [str(x[0]) for x in user_avatar]
            pk = request.parser_context['kwargs']['pk']
            return bool(pk in alls)
        else:
            return True
    
# 定义具体的增删查改权限限制
class UserViewsetPermissions(BasePermission):
    def has_permission(self,request,view):
        if request.method == "GET":
            pk = None
            try:
                pk = request.parser_context['kwargs']['pk']
            except:
                pass
            if pk is not None:
                if int(request.user.pk) == int(pk):
                    return True
            else:
                return True
            group = Group.objects.filter(name='管理员').first()
            return bool(group in request.user.groups.all())   #　返回布尔值
        elif request.method == "POST":
            permissions = Permission.objects.filter(codename='add_user').first()
            return bool(permissions in request.user.user_permissions.all() and request.user)
        elif request.method == "DELETE":
            permissions = Permission.objects.filter(codename='delete_user').first()
            return bool(permissions in request.user.user_permissions.all() and request.user)
        elif request.method == "PUT":  # 可编辑自身---其他用户编辑需要权限  编辑用户
            pk = request.parser_context['kwargs']['pk']
            if int(request.user.pk) == int(pk):
                return True
            permissions = Permission.objects.filter(codename='change_user').first()
            return bool(permissions in request.user.user_permissions.all() and request.user)
            # group = Group.objects.filter(name='管理员').first()
            # return bool(group in request.user.groups.all())   #　返回布尔值

# 权限增删查改
class PermissionViewsetPermissions(BasePermission):
    def has_permission(self,request,view):
        if request.method == "GET":
            if request.user:
                return True
        elif request.method == "POST":
            return False   # 暂未开放此功能
            permissions = Permission.objects.filter(codename='add_permission').first()
            return bool(permissions in request.user.user_permissions.all() and request.user)
        elif request.method == "DELETE":
            return False   # 暂未开放此功能
            permissions = Permission.objects.filter(codename='delete_permission').first()
            return bool(permissions in request.user.user_permissions.all() and request.user)
        elif request.method == "PUT":  
            return False   # 暂未开放此功能
            permissions = Permission.objects.filter(codename='change_permission').first()
            return bool(permissions in request.user.user_permissions.all() and request.user)

# 组增删查改
class GroupViewsetPermissions(BasePermission):
    def has_permission(self,request,view):
        if request.method == "GET":
            if request.user:
                return True
        elif request.method == "POST":
            permissions = Permission.objects.filter(codename='add_group').first()
            return bool(permissions in request.user.user_permissions.all() and request.user)
        elif request.method == "DELETE":
            permissions = Permission.objects.filter(codename='delete_group').first()
            return bool(permissions in request.user.user_permissions.all() and request.user)
        elif request.method == "PUT":  
            permissions = Permission.objects.filter(codename='change_group').first()
            return bool(permissions in request.user.user_permissions.all() and request.user)


# 登陆日志查看与删除
class LoginLogPermissions(BasePermission):
    def has_permission(self,request,view):
        if request.method == "GET" or request.method == "DELETE":
            if request.user :
                return True
            else:
                return False
        else :
            False


# 登陆接口访问权限 -- 加上黑名单不给登的限制  -- 只提供post方法
class LoginPermissions(BasePermission):
    def has_permission(self,request,view):
        if request.method == "POST":
            if BlackUser.objects.filter(bname=request.data["usr"]).count() > 0 or BlackUser.objects.filter(bphone=request.data["usr"]).count() > 0 :
                return False
            else:
                return True
        else:
            return False
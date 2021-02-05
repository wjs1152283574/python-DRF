from django.shortcuts import render
from rest_framework import permissions, exceptions
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission,Group 
from .models import User,UserAvatar,LogonLog,Departments
from .serializers import * 
from .permissions import * 
from .throttle    import *

# 用户详情/注册视图继承了mixins扩展类--想使用扩展类必须也继承viewsets.GenericViewSet
class UserViewset(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    """
    User-Register--Only Post
    """
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes     = [UserViewsetPermissions,permissions.IsAuthenticated]
    def get_queryset(self):
        group = Group.objects.filter(name='管理员').first()
        alls = [str(x[1]) for x in self.request.user.groups.all().values_list()]
        if str(group) in alls:
            queryset = User.objects.all()
        else:
            queryset = User.objects.filter(username=self.request.user.username)
        return queryset

    # retrieve
    def get_object(self):
        pk = self.request.parser_context['kwargs']['pk']
        group = Group.objects.filter(name='管理员').first()
        alls = [str(x[1]) for x in self.request.user.groups.all().values_list()]
        if str(group) in alls:
            return User.objects.filter(pk=pk).first()
        else:
            return self.request.user
        
    def get_serializer_class(self):
        if self.action == "update":
            group = Group.objects.filter(name='管理员').first()
            alls = [str(x[1]) for x in self.request.user.groups.all().values_list()]
            if str(group) in alls:
                serializer_class = UserBaseInfosUpdateSerializers
            else:
                pk = self.request.parser_context['kwargs']['pk']
                if int(self.request.user.pk) == int(pk):
                    serializer_class = UserUpdateSerializers  
                # else:
                #     serializer_class = UserBaseInfosUpdateSerializers
        else:
            serializer_class = UserRegisterSerializer
        return serializer_class

# 用户组视图
class BMS_GroupViewset(viewsets.ModelViewSet):
    queryset           = Group.objects.all()
    permission_classes = [GroupViewsetPermissions,permissions.IsAuthenticated]
    pagination_class   = None
    throttle_classes   = [UserViewsetThrottle]
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve" :
            serializer_class = BMS_GroupSerializers_get
        else:
            serializer_class = BMS_GroupSerializers_post
        return serializer_class
# 权限
class Bms_PermissionViewset(viewsets.ModelViewSet):
    queryset           = Permission.objects.all()
    permission_classes = [PermissionViewsetPermissions]
    pagination_class   = None
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            serializer_class = Bms_PermissionSerializers_get
        else:
            serializer_class = Bms_PermissionSerializers_post
        return serializer_class

# 只读，新增权限时需要
class ContentypesViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    queryset = ContentType.objects.all()
    serializer_class = ContentypesSerializers
    permission_classes = [permissions.IsAuthenticated]

class UserAvatarViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin):
    serializer_class = UserAvatarSerializers
    permission_classes = [permissions.IsAuthenticated,AvatarPermission]

    def get_queryset(self):
        user = self.request.user
        return UserAvatar.objects.filter(user=user)
    
    # 创建人为当前用户
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
# 手动签发 token  以限制登陆接口访问次数及配合系统黑名单来控制登陆权限 以及写入登陆日志信息
# 一天可访问登陆接口五次--在settings里配置限制次数  "test_casso":"5/day",
class LoginViews(APIView):
    permission_classes = [LoginPermissions]
    authentication_classes = []
    throttle_classes = [UserViewsetThrottle]
    def post(self, request, *args, **kwargs):
        user_ser = LoginSerializersp(data=request.data)

        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            ip = request.META.get("REMOTE_ADDR")

        os = request.META.get("OS")
        usr = request.data.get('usr')
        agent = request.META.get("HTTP_USER_AGENT")

        if user_ser.is_valid():
            log_data = {"usr_str":usr,"remote_addr":ip,"agent":agent,"os":os,"status":1}
        else :
            log_data = {"usr_str":usr,"remote_addr":ip,"agent":agent,"os":os,"status":0}

        login_log = LogonLogSerializers(data=log_data)
        if login_log.is_valid():login_log.save()

        #  手动签发 token 
        user_ser.is_valid(serializers.ValidationError)
        res = {"token":user_ser.token}
        return Response(data=res,status=200)

# 登录日志视图集 -- 在自定义权限类中限制了请求方法 get  delete 其他方法不支持(403)
class LoginLogViewset(viewsets.ModelViewSet):
    queryset = LogonLog.objects.all()
    serializer_class = LogonLogSerializers
    pagination_class = None
    permission_classes = [LoginLogPermissions,permissions.IsAuthenticated]  # 权限限制只能查看--all user

# 部门接口视图集
class DeparViewsets(viewsets.ModelViewSet):
    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializers
    pagination_class = None


# 系统黑名单
class BlackUserViewsets(viewsets.ModelViewSet):
    queryset = BlackUser.objects.all()
    serializer_class = BlackUserSerializers_post
    pagination_class = None

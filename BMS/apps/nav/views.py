from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.http import HttpResponse
from .models import BaseNav,Icons,SecondNav,ThirtNav
from .serializers import BaseNavSerializers_get,BaseNavSerializers_post,IconsSerializers,SecondNavSerializers,ThirtNavSerializers
from .Elementui_icons import icon_data
from .permissions import CheckAdmin,SipecalPermissions
# Create your views here.

#　导入icon数据
def migrateIcons(request):
    for item in icon_data:
        iconInstance = Icons()
        iconInstance.icon_belong = item["icon_belong"]
        iconInstance.icon = item["icon"]
        iconInstance.save()
    return HttpResponse("add-icons-successfully!")

class BaseNavViewset(viewsets.ModelViewSet):
    '''
    主菜单
    '''
    queryset = BaseNav.objects.all()

    permission_classes = [SipecalPermissions]  # 使用自定义权限类 配合框架自带权限类使用，都返回False就是没有权限
    authentication_classes = [JSONWebTokenAuthentication]  # 采用JWT来进行用户认证  
    def get_serializer_class(self):
        if self.action == "list":
            serializer_class = BaseNavSerializers_get
        else:
            serializer_class = BaseNavSerializers_post
        return serializer_class
    # 创建人为当前用户
    def perform_create(self, serializer):
        serializer.save(add_user=self.request.user)
    
class IconsViewset(viewsets.ModelViewSet):
    '''
    菜单图标
    '''
    queryset = Icons.objects.all()
    serializer_class = IconsSerializers
    permission_classes = [SipecalPermissions]
    pagination_class = None  # 前段自定义每页显示数量?limit=n

class SecondNavViewset(viewsets.ModelViewSet):
    '''
    二级菜单
    '''
    serializer_class = SecondNavSerializers
    permission_classes = [SipecalPermissions]
    # 创建人为当前用户
    def perform_create(self, serializer):
        serializer.save(sadd_user=self.request.user)
    
    def get_queryset(self):
        parent_nav_id = self.request.query_params.get("parentid",None)
        if parent_nav_id is not None:
            queryset = SecondNav.objects.filter(parannav=parent_nav_id)
        else:
            queryset = SecondNav.objects.all()
        return queryset

class ThirtNavViewset(viewsets.ModelViewSet):
    '''
    二级菜单
    '''
    serializer_class = ThirtNavSerializers
    permission_classes = [SipecalPermissions]
    # 创建人为当前用户
    def perform_create(self, serializer):
        serializer.save(tadd_user=self.request.user)
    
    def get_queryset(self):
        parent_nav_id = self.request.query_params.get("parentid",None)
        if parent_nav_id is not None:
            queryset = ThirtNav.objects.filter(parannav=parent_nav_id)
        else:
            queryset = ThirtNav.objects.all()
        return queryset
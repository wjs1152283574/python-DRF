# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2020 Casso.Wong
#      Author:  Casso.Wong
# Start  Date:  2020/05/31
# Last modify: 
#
##############################################################################

'''
    自定义用户认证类

'''

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .import models

class UsersAuth(BaseAuthentication):
    def authenticate(self,request):
        auth = request.META.get('HTTP_AUTHORIZATION',None)

        # 游客
        if auth is None:
            return None
            
        auth_list = auth.split() 
        if not (auth_list[0] != 'auth' and auth_list[1] != 'casso.admin'):
            raise AuthenticationFailed('认证信息有误，非法用户')

        user = models.User.objects.filter(username="casso").first()
        if not user:
            raise AuthenticationFailed('用户信息有误，非法用户')
        
        return (user,None)

# 登陆接口认证类--记录登陆日志(成功与失败)
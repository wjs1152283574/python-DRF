from django.db import models
from apps.users.models import User
# Create your models here.

# 所有图标类名：目前只支持Elementui 图标(爬取地址：https://element.eleme.io/#/zh-CN/component/icon)
class Icons(models.Model):
    objects = models.Manager()
    icon = models.CharField('图标类名',max_length=40,null=False)
    icon_belong = models.CharField('菜单所属UI',max_length=15)
    class Meta:
        verbose_name = "图标"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.icon

# 主菜单模型 : 包含菜单名以及菜单icon (Elementui) 
# 实现功能： 菜单名以及菜单icon可自定义--后续还会实现按钮基色控制
class BaseNav(models.Model):
    objects = models.Manager()
    nav_name = models.CharField('主菜单名',max_length=30,null=False)
    nav_icon = models.ForeignKey(Icons,on_delete=models.SET_NULL,null=True, related_name="主菜单图标")
    add_time = models.DateTimeField("添加时间", auto_now_add=True)
    add_user = models.ForeignKey(User,related_name="创建人",on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name = "主菜单"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.nav_name
# 二级菜单
class SecondNav(models.Model):
    objects = models.Manager()
    snav_name = models.CharField('二级菜单',max_length=40)  # 10个汉字
    parannav  = models.ForeignKey(BaseNav,on_delete=models.CASCADE,related_name='父菜单')
    snav_icon = models.ForeignKey(Icons,on_delete=models.SET_NULL,null=True,related_name='二级菜单')
    sadd_time = models.DateTimeField('添加时间',auto_now_add=True)
    sadd_user = models.ForeignKey(User,related_name='二级菜单创建人',on_delete=models.DO_NOTHING)
    
    @property
    def icon_name(self):
        return self.snav_icon.icon
    
    class Meta:
        verbose_name = "二级菜单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.snav_name

# 三级菜单
class ThirtNav(models.Model):
    objects = models.Manager()
    tnav_name = models.CharField('三级菜单',max_length=40)  # 10个汉字
    parannav  = models.ForeignKey(SecondNav,on_delete=models.CASCADE,related_name='父菜单')
    tnav_icon = models.ForeignKey(Icons,on_delete=models.SET_NULL,null=True,related_name='三级菜单')
    tadd_time = models.DateTimeField('添加时间',auto_now_add=True)
    tadd_user = models.ForeignKey(User,related_name='三级菜单创建人',on_delete=models.DO_NOTHING)
    @property
    def icon_name(self):
        return self.tnav_icon.icon
    class Meta:
        verbose_name = "三级菜单"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.tnav_name
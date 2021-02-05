from django.db import models
from datetime import datetime

# Create your models here.
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.contrib.contenttypes.models import ContentType


class Departments(models.Model):
    DEP_TYPR = (
        (1,"总经办"),
        (2,"部门"),
        (3,"班组"),
    )
    objects = models.Manager()
    depar_name = models.CharField("部门名称",max_length=40,unique=True)
    depar_type = models.IntegerField("部门类型",choices=DEP_TYPR,default=2)
    class Meta:
        db_table = "bms_depar"
        verbose_name = "部门表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.depar_name

# 自定义数据模型--继承与框架原本的用户模型
class User(AbstractUser):
    #  使用choices属性的用处：在序列化器中自定义字段时可以使用get_sex_display() 来返回SEX_CHOISE中元组的最后一项
    # 用法实例看序列化器
    SEX_CHOISE = (
        (1,"男"),
        (2,"女")
    )
    mobile = models.CharField("电话", max_length=11, unique=True)
    email  = models.EmailField("邮箱", blank=True, null=True)
    sex    = models.IntegerField("性别",choices=SEX_CHOISE,default=1)
    # sex = models.BooleanField("性别", default=True, blank=False, null=False) # 效果一致
    age    = models.IntegerField("年龄", default=18, blank=True, null=True)
    icon   = models.ImageField(upload_to="icon",default="icon/defult.png")
    depar  = models.ForeignKey(Departments,on_delete=models.CASCADE,null=True,blank=True)
    class Meta:
        db_table = "bms_users"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

# 用户头像
class UserAvatar(models.Model):
    objects = models.Manager()
    avatar  = models.ImageField(upload_to="avatar",default="icon/defult.png")
    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table = "bms_users_avatar"
        verbose_name = "用户头像"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.user

# 日志模型
class LogonLog(models.Model):
    objects = models.Manager()
    usr_str = models.CharField(max_length=50)
    remote_addr = models.CharField(max_length=20)
    agent = models.CharField(max_length=100)
    ace_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)
    os = models.CharField(max_length=30)
    class Meta:
        db_table = "bms_login_log"
        verbose_name = "登录日志"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.usr_str

# 黑名单模型
class BlackUser(models.Model):
    objects = models.Manager()
    bname = models.CharField(max_length=50)
    bphone = models.CharField(max_length=11)
    remark = models.CharField(max_length=100)
    add_time = models.DateTimeField(auto_now_add=True)
    add_usr = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    class Meta:
        db_table = "bms_black_user"
        verbose_name = "系统黑名单"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.bname
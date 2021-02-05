from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission,Group 
from .models import User,Departments,UserAvatar,LogonLog,BlackUser
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.utils import jwt_encode_handler,jwt_payload_handler
import re

# 手机号码正则表达式
REGEX_MOBILE = r"^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

# 权限--get
class Bms_PermissionSerializers_get(serializers.ModelSerializer):
    class Meta:
        model  = Permission
        fields = "__all__"
        depth  = 1
# 权限--post
class Bms_PermissionSerializers_post(serializers.ModelSerializer):
    class Meta:
        model  = Permission
        fields = "__all__"
        # depth  = 1

# 用户注册序列化器--验证用户是否已存在、验证手机号码是否已存在、合法手机号、加密保存用户信息（password）
class UserRegisterSerializer(serializers.ModelSerializer):
    # user_permissions = Bms_PermissionSerializers()
    # 验证用户名是否存在
    username = serializers.CharField(
        label="用户名",
        help_text="用户名",
        required=True,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")],
    )
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, required=True, label="密码"
    )
    # 重写sex字段---对应模型中的SEX_CHOISE
    # 这种情况交给前端去处理会更方便--比如Elementui 中的<el-option>就会有对应的value跟label
    # sex = serializers.SerializerMethodField()
    # def get_sex(self,obj):
    #     return obj.get_sex_display()
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}
        depth = 1

    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_mobile(self, mobile):
        # 是否已经注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")
        # 是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")
        return mobile

    # 密码验证--目前只验证过短密码其它不做限制
    def validate_password(self, password):
        if len(password) >= 5:
            return password
        else:
            raise serializers.ValidationError("密码过短")

# 用户组-post
class BMS_GroupSerializers_post(serializers.ModelSerializer):
    class Meta:
        model  = Group
        fields = [
            "pk",
            "name",
            "permissions"
        ]
# 用户组-get
class BMS_GroupSerializers_get(serializers.ModelSerializer):
    class Meta:
        model  = Group
        fields = [
            "pk",
            "name",
            "permissions"
        ]
        depth = 1

class UserBaseInfosUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "pk",
            "username",
            "is_superuser",
            "is_staff",
            "is_active",
            "mobile",
            "email",
            "depar",
            "groups",
            "user_permissions"
        ]
        read_only_fields = ['password']

class UserUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "mobile",
            "email"
        ]

class DepartmentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = [
            "pk",
            "depar_name",
            "depar_type"
        ]

class UserAvatarSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAvatar
        fields = [
            "pk",
            "avatar",
            "user"
        ]
        read_only_fields = ['user','pk']

class ContentypesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"

class LoginSerializersp(serializers.ModelSerializer):
    usr = serializers.CharField(write_only=True)
    pwd = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["usr","pwd"]
    
    def validate(self,attrs):
        usr = attrs.get("usr")
        pwd = attrs.get("pwd")

        if usr and re.match(REGEX_MOBILE,usr):
            user = User.objects.filter(mobile=usr).first()
        else:
            user = User.objects.filter(username=usr).first()
        
        if user and user.check_password(pwd) :
            self.token = jwt_encode_handler(jwt_payload_handler(user))
            return attrs
        
        raise serializers.ValidationError({"data":"登陆信息不可用"})

# 登录日志序列化器
class LogonLogSerializers(serializers.ModelSerializer):
    class Meta:
        model = LogonLog
        fields = [
            "pk",
            "usr_str",
            "remote_addr",
            "agent",
            "status",
            "os",
            "ace_time"
        ]
        read_only_fields = ['pk','ace_time']

class BlackUserSerializers_post(serializers.ModelSerializer):
    class Meta:
        model = BlackUser
        fields = "__all__"
        read_only_fields = ['pk','add_time']
        # depth = 1
        # fields = [
        #     "pk",
        #     "bname",
        #     "bphone",
        #     "add_time",
        #     "add_usr"
        # ]

        
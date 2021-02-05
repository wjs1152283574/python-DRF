
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.views import APIView
from apps.nav import views as NavViewset
from apps.users import views as userviews
# 统一管理url
# 需要配置media访问路径
from django.views.static import serve
from BMS.settings import MEDIA_ROOT

# NAV

from rest_framework import routers
router = routers.DefaultRouter()
# 用户注册接口  用户详情
router.register(r"bms/user", userviews.UserViewset, basename="user")
router.register(r"bms/groups", userviews.BMS_GroupViewset, basename="group")
router.register(r"bms/permissions", userviews.Bms_PermissionViewset, basename="permission")
router.register(r"bms/contenttype",userviews.ContentypesViewset,basename="contype")
router.register(r"bms/nav", NavViewset.BaseNavViewset, basename="nav")
router.register(r"bms/icon", NavViewset.IconsViewset, basename="icon")
router.register(r"bms/snav", NavViewset.SecondNavViewset, basename="snav")
router.register(r"bms/tnav", NavViewset.ThirtNavViewset, basename="tnav")
router.register(r"bms/avatar",userviews.UserAvatarViewset,basename="avatar")
router.register(r"bms/loginlog",userviews.LoginLogViewset,basename="loginlog")
router.register(r"bms/depar",userviews.DeparViewsets,basename="depar")
router.register(r"bms/blackusr",userviews.BlackUserViewsets,basename="blackusr")
urlpatterns = [
    path('bms/admin/', admin.site.urls),
    path("", include(router.urls)),
    # 测试阶段api页面的登录接口(测试页面右上角的login)
    path(r"api-auth/", include("rest_framework.urls")),
    # path("bms/login/", obtain_jwt_token),  # 自动签发token
    path("bms/login/",userviews.LoginViews.as_view()),
    # path("bms/addicons/",NavViewset.migrateIcons),
    path("bms/media/<path:path>", serve, {"document_root": MEDIA_ROOT}),
]

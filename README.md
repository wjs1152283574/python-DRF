# 后台管理系统

#### 介绍
后台管理系统 DRF webpack py3   
超管：casso casso
#### 软件架构
1.   `python -m pip install --upgrade pip`   #　pip 升级到pip3

2.   `pip3 freeze > requirements.txt`  # 收集依赖  建议每次上传代码先收集一下，以免其他成员环境缺少新增依赖

3.   `pip3 install -r requirements.txt`  #　报依赖缺失时运行

4.   `CREATE DATABASE `bms` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;` # mysql建表

5.   `python manage.py dumpdata > bms_data.json`    # 导出数据库中的数据，木有指定app即导出所有app数据

6.   `python manage.py loaddata bms_data.json`      # 导入现有数据, 数据库迁移文件太多会可能会迁移出错 导出 删库 重建 导入

7.   在云服务器上迁移数据库 : `python3 manage.py makemigrations/python3 manage.py migrate`  (需要用python3 执行)


### 代码提交`tips`：

  2.  打开`git bash`
  3.  输入`ssh-keygen -t rsa -C "你的邮箱地址"` 三次回车之后就可以生成密钥对
  4.  输入`cat ~/.ssh/id_rsa.pub` 查看你的 public key（公钥）复制粘贴到码云即可



#### 项目定位：云办公平台

### ############### 项目模块概述 #########################

#### 一：基础模块

1.  用户管理模块 
2.  菜单管理模块
3.  日志管理模块
4.  用户组管理模块
5.  权限管理模块
6.  图像素材管理模块
7.  部门管理模块
8.  系统黑名单模块

#### 二：基本功能模块

1.  企业通讯录管理功能模块
   * 推送功能:`websocket` ; 聊天室
   * `pip3 install channels==2.3`
   * 创建对应的`routing`模块(`urls`模块同级); `settings`注册`channel`; `settings`配置`application`模块
   * 创建对应的app: `cd apps;  django-admin startapp addrbook;` 
   * 创建asgi模块; nginx配置当作正常的接口路由配置即可 `location /websocket/`{指定监听端口以及其他配置} 
2.  考勤管理功能模块
3.  日程安排功能模块
4.  工作汇报功能模块
5.  审批/审批流程管理功能模块
6.  外勤人员定位轨迹功能模块
7.  公告/公告系统管理功能模块
8.  企业文化宣传/培养专栏功能模块
   

#### Commit 规范

###### 格式如下
* 例：`fead(type)`:本次提交概述
* `type`: 本次 commit 的类型，诸如 bugfix docs style 等，参考如下:

    * `fead`：添加新功能
    * `fix`：修补缺陷
    * `docs`：修改文档
    * `style`：修改格式
    * `refactor`：重构
    * `perf`：优化
    * `test`：增加测试
    * `chore`：构建过程或辅助工具的变动
    * `revert`：回滚到上一个版本

* `scope`: 本次 `commit` 波及的范围
* `subject`: 简明扼要的阐述下本次 `commit` 的主旨，在原文中特意强调了几点：

    1. 使用祈使句，是不是很熟悉又陌生的一个词
    2. 首字母不要大写
    3. 结尾无需添加标点

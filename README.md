# Django Rest_framework + Vue  打造生鲜超市
## 掌握技术
1. Vue+Django Rest_Framework前后端分离技术
2. 彻底玩转restful api 开发流程
3. Django Rest Framework 的功能实现和核心源码分析

## 系统构成
1. Vue 前端
2. Django Rest_framework 实现前台功能
3. xadmin 后台管理系统
```
    1. 安装最新版的 django
    2. 安装最新版的xadmin
    pip install xadmin2
    3. 更改路由
    from django.urls import path, include
    import xadmin

    xadmin.autodiscover()
    urlpatterns = [
        # path('admin/', admin.site.urls),
        path('xadmin/', xadmin.site.urls),
    ]
    4.生成数据库
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
```

### vue部分
1. API 接口
2. Vue 与 api 交互
3. Vue 相许组织结构分析

### Django Rest_framework 技能
- 通过 view 实现rest api接口
- genericView 方式实现接口
- Vuewset 盒router 方式实现api接口和url配置

## Django虚拟环境项目搭建
    1. 安装虚拟环境包
        ```
            pip install virtualenv

            pip install virtualenvwrapper-win
        ```
    2. 创建虚拟环境
        ```
            mkvirtualenv 虚拟环境的项目名
        ```
    3. 查看有哪些虚拟环境
        ```
            workon 
        ```
    4. 进入虚拟环境
        ```
            workon DjangoProject
        ```
    5. 退出虚拟环境
        ```
            deactivate.bat
        ```
    6. 激活虚拟环境
        ```
            activate.bat
        ```
## Vue 环境搭建
1. [下载node.js](https://nodejs.org/en/)
2. 安装淘宝源的npm脚手架
    ```
        npm install -g cnpm --registry=https://registry.npm.taobao.org
    ```
3. 安装依赖
    ```
        npm install
    ```
4. 运行项目
    ```
        npm run serve
    ```

import xadmin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token

xadmin.autodiscover()

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls), # 后台管理
    path('goods/', include("goods.urls")),  # django后端返回的
    path('docs', include_docs_urls(title="星尘科技")), # 进入drf
    path('api-auth/', include('rest_framework.urls')), # api认证
    path('api-goods/', include('goods.urls_api')), # django_restfroamework 后端返回的数据
    path('api-token-auth/', obtain_auth_token), # 使用drf中的token
    path('jwt-auth/', obtain_jwt_token, name="login"), # jwt的认证接口 jwt json web token
    path('api-users/', include('users.urls')), # 系统用户
    path('api-user_operation/', include('user_operation.urls')), # 用户操作接口
    path('api-trade/', include('trade.urls')) # 购物车类
]

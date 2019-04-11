import xadmin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

xadmin.autodiscover()

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls), # 后台管理
    path('goods/', include("goods.urls")),  # django后端返回的
    path('docs', include_docs_urls(title="星尘科技")), # 进入drf
    path('api-auth/', include('rest_framework.urls')), # api认证
    path('api/goods/', include('goods.urls_api')), # django_restfroamework 后端返回的数据
    path('api-token-auth/', obtain_auth_token)
]






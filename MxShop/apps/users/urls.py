from django.urls import path, include, re_path
from users.view.VerifyView import SmsCodeViewset, UserViewset
from rest_framework.routers import DefaultRouter # 集成方式定义urls

# ViewSets 和 Routers 结合使用
router = DefaultRouter()

# 配置goods 的url 注册视图
router.register(r'code', SmsCodeViewset, base_name="code")
router.register(r'users', UserViewset, base_name="users")


# 注册路由
urlpatterns = [
	# path('goods_list/', GoodsListView.as_view(), name="goods"), # 所有商品列表
	re_path(r'^', include(router.urls)),
]

from django.urls import path, include, re_path
from goods.views_api.GoodView import GoodsListViewSet # 商品列表
from goods.views_api.GoodCategoryView import CategoryViewSet # 商品类别
from rest_framework.routers import DefaultRouter # 集成方式定义urls

# ViewSets 和 Routers 结合使用
router = DefaultRouter()

# 配置goods 的url 注册视图
router.register('goods_list', GoodsListViewSet)
router.register(r'categorys', CategoryViewSet, base_name="categorys")

# 注册路由
urlpatterns = [
	# path('goods_list/', GoodsListView.as_view(), name="goods"), # 所有商品列表
	re_path(r'^', include(router.urls)),
]

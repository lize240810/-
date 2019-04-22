from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter # 集成方式定义urls
from trade.view.TradeView import ShoppingCartView
from trade.view.OrderView import OrderViewset
# ViewSets 和 Routers 结合使用
router = DefaultRouter()

# 配置goods 的url 注册视图

router.register(r'shopping_cart', ShoppingCartView, base_name="shopping_cart")
router.register(r'order', OrderViewset, base_name="order") # 订单


# 注册路由
urlpatterns = [
	# path('goods_list/', GoodsListView.as_view(), name="goods"), # 所有商品列表
	re_path(r'^', include(router.urls)),
]

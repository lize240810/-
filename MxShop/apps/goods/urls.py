from django.urls import path, include

from goods.views.GoodsView import GoodsListView 


urlpatterns = [
	path('goods_list/', GoodsListView.as_view(), name="goods"), # 所有商品列表
]

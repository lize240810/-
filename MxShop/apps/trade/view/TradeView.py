from rest_framework import viewsets, mixins, status # 渲染
from rest_framework.permissions import IsAuthenticated # 认证
from rest_framework_jwt.authentication import JSONWebTokenAuthentication # 认证
from rest_framework.authentication import SessionAuthentication # 登录认证

from trade.models import ShoppingCart, OrderGoods
from trade.serializers import ShopSerializer, ShopCartDetailSerializer # 序列化
from utils.permissions import IsOwerOrReadOnly


class ShoppingCartView(viewsets.ModelViewSet):
    """
        购物车功能
        list: 购物车详情
        create: 加入购物车
        delete: 删除商品
        read: 查询某个商品
    """
    # 判断是否够登录 是否是当前用户
    permission_classes = (IsAuthenticated, IsOwerOrReadOnly)
    # 
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopSerializer
    #商品的id
    lookup_field = "goods_id"

    def get_queryset(self):
        # 购物车商品
        return ShoppingCart.objects.filter(user=self.request.user)

    # 动态选怎serializer
    def get_serializer_class(self):
        # print("---"*50, self.action)
        if self.action == 'list' or self.action == 'retrieve':
            return ShopCartDetailSerializer
        else:
            return ShopSerializer
    

from rest_framework import viewsets, mixins, status # 渲染
from rest_framework_jwt.authentication import JSONWebTokenAuthentication # 认证
from rest_framework.authentication import SessionAuthentication # 登录认证
from rest_framework.permissions import IsAuthenticated # 认证

from trade.models import OrderInfo
from trade.serializers import OrderGoodsSerializer, OrderDetailSerializer, OrderSerializer
from utils.permissions import IsOwerOrReadOnly

class OrderViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
	"""订单管理
		list: 订单列表
		delete: 删除订单
		create: 创建订单
	"""
	# 用户登录 是否是当前用户
	permission_classes = (IsAuthenticated, IsOwerOrReadOnly)
	# 登录以后验证
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	serializer_class = OrderSerializer
	# 动态配置serializer

	def get_serializer_class(self):
		# 如果是检索就使用 订单嵌套商品的系列化
		if self.action == 'retrieve':
			return OrderDetailSerializer

		return OrderSerializer

	# 获订单列表
	def get_queryset(self):
		# import ipdb; ipdb.set_trace()
		return OrderInfo.objects.filter(user=self.request.user)





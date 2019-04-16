from rest_framework import viewsets, mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from user_operation.serializers import UserFavSerializers, UserFavDetailSerializer, LeavingMessageSerializer, AddressSerializers
from utils.permissions import IsOwerOrReadOnly  # 用户自定义权限


class UserFavViewset(
        viewsets.GenericViewSet,
        mixins.ListModelMixin,  # 获取已收藏的商品列表
        mixins.DestroyModelMixin,  # 取消收藏（相当于数据库删除）
        mixins.CreateModelMixin  # 添加收藏(相当于创建数据库)
        # mixins.RetrieveModelMixin
):
    """
        商品收藏
        list: 收藏列表
        create: 收藏商品
        delete: 取消收藏
    """
    '''
		加入了权限认证
		1. 只有认证用户才可以收藏
		2. 用户只能获取自己的收藏，不能获取素有用户的收藏
		3. JSONWebTokenAuthentication 认证不应该全局配置，因为用户获取商品信息或其他页面时不需要认证，只需要在局部中添加就可以
	'''
    # queryset = UserFav.objects.all()
    # 判断输入的序列化
    serializer_class = UserFavSerializers
    # permission 是用来做权限判断的
    # IsAuthenticated： 必须是登录用户 ； IsownerOrReadOnly 必须是当前登录用户
    permission_classes = (IsAuthenticated, IsOwerOrReadOnly)
    # auth 使用用户认证
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication)
    # 搜索字段
    lookup_field = 'goods_id'

    def get_queryset(self):
        # import ipdb;ipdb.set_trace()
        # 查询收藏列表 根据当前登录用户来进行收藏呢 只查询自己的
        return UserFav.objects.filter(user=self.request.user)

    # 动态选择 serializer
    def get_serializer_class(self):
        # import ipdb; ipdb.set_trace()
        if self.action == 'list':
            '''
                    数据结果为列表的时候进行与商品序列化进行嵌套展示收藏的商品
            '''
            return UserFavDetailSerializer
        elif self.action == 'create':
            # 收藏商品的时候没有与商品进行嵌套直接收藏商品id即可
            return UserFavSerializers
        return UserFavSerializers


class LeavingMessageViewset(
        viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin):
    """
        list: 获取用户留言
        create: 添加留言
        delete: 删除留言
    """
    permission_classes = (IsAuthenticated, IsOwerOrReadOnly)  # 用户自定义权限
    # 序列化用户
    serializer_class = LeavingMessageSerializer
    # 认证用户
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        # 只看自己的留言
        print('-' * 20, self.request.user, '-' * 20)
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressSerializers(
    viewsets.GenericViewSet, mixins.CreateModelMixin,
    mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    """
        list: 收货地址列表
        create: 添加收货地址
        delete: 删除收货地址
        update: 更新收货地址
    """
    # 用户认证 IsAuthenticated： 必须是登录用户 ； IsownerOrReadOnly 必须是当前登录用户
    permission_classes = [IsAuthenticated, IsOwerOrReadOnly]
    # 使用认真
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication)
    # 指定序列化
    serializer_class = AddressSerializers

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

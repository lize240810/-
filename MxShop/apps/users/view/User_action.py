import random

from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication, permissions
from rest_framework_jwt.serializers import (
    jwt_encode_handler, # 编译为
    jwt_payload_handler # 转换为字典类型
)

from users.serializers import UserRegSerializer, UserDetailSerializer # 手机号码验证  #  会员详细信息

from users.models import VerifyCode
from utils.yuntongxun import message_validate # 发送短息你的方法
# from utils.permission import IsOwerOrReadOnly

User = get_user_model()

class UserViewset(
    mixins.CreateModelMixin, # 创建使用
    mixins.UpdateModelMixin, # 修改使用
    mixins.RetrieveModelMixin, # 获取用户信息
    viewsets.GenericViewSet
):
    '''
        用户注册
        create: 用户注册
        read: 根据id查询用户详细信息
        update: 用户信息修改
        partial_update: 用户查询并修改
    '''
    serializer_class = UserRegSerializer # 指定序列化类
    queryset = User.objects.all() # 数据集
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication) # 身份验证
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)

        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 动态权限配置
    '''
        1. 用户注册的时候不应该有权限限制
        2. 想要获取用户相信信息的时候必须登录
    '''
    def get_permissions(self):
        # 检索的时候就必须通过一个验证
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        # 创建用户就取消验证
        elif self.action == "create":
            return []
        return []
    
    # 动态选择序列化的方式
    '''
        1. UserRegSerializer 用户注册, 只返回username 和 mobile ，
        会员中心页面需要显示多个字段，
        所以需要创建一个UserDetailSerializer
        2. 注册使用userdetailSerializer 又会导致失败，所以需要配置动态的
    '''
    def get_serializer_class(self):
        # 检索（查询）
        if self.action == 'retrieve':
            # 显示使用直接进行字段显示即可
            return UserDetailSerializer
        elif self.action == 'create':
            # 注册使用的 需要进行验证指定字段
            return UserRegSerializer

        return UserDetailSerializer

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()

        
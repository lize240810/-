import random

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from utils.yuntongxun import message_validate # 发送短息你的方法
from users.serializers import SmsSerializer # 手机号码验证
from users.models import VerifyCode
from rest_framework_jwt.serializers import (
    jwt_encode_handler, # 编译为
    jwt_payload_handler # 转换为字典类型
    )
from django.contrib.auth import get_user_model
User = get_user_model()


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """手机验证码"""
    serializer_class = SmsSerializer

    def generate_code(self):
        '''
            生成四位数验证码
        '''
        return ''.join(random.sample(list('0123456789'),4))


    def create(self, request, *args, **kwargs):
        # 序列化验证
        serializer = self.get_serializer(data=request.data)
        #验证合法
        serializer.is_valid(raise_exception=True)
        
        # 获取号码
        mobile = serializer.validated_data['mobile']
        # 验证码
        code = self.generate_code()
        # 发短信
        yun_xun = message_validate(phone_number=mobile, validate_number=code)
        if not yun_xun[0]:
            return Response({
                # 返回错误消息
                'mobile': yun_xun[-1],
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_recode = VerifyCode(code=code, mobile=mobile)
            code_recode.save()
            return Response({
                'mobile': mobile,
                }, status=status.HTTP_201_CREATED)


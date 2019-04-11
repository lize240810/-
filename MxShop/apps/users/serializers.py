# 序列化
import re
from datetime import datetime, timedelta 
from MxShop.settings import REGEX_MOBILE # 验证手机号
from .models import VerifyCode # 验证码模型类
from rest_framework import serializers 
from django.contrib.auth import get_user_model
User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    # 函数验证
    #函数名必须：validate + 验证字段名
    def validate_mobile(self, mobile):

        # import ipdb; ipdb.set_trace()
        # 是否已注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证发送频率
        # 验证码发送频率
        #60s内只能发送一次
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)

        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile
# 序列化
import re
from datetime import datetime, timedelta 
from MxShop.settings import REGEX_MOBILE # 验证手机号
from .models import VerifyCode # 验证码模型类
from user_operation.models import UserFav
from rest_framework import serializers 
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from goods.serializers import GoodsSerializer
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


class UserRegSerializer(serializers.ModelSerializer):
    """用户注册"""
    # 用户表中没有验证码字段，需要自定义一个 输入时验证的
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, 
        label="验证码",
        error_messages={
            "blank": "请输入验证码",
            "required": "请输入验证码",
            "max_length": "验证码格式错误",
            "min_length": "验证码格式错误",
    })
    
    # 判断用户验证码是否存在
    username = serializers.CharField(
        label="用户名",  
        required=True, 
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")]
    )
    

    # import ipdb; ipdb.set_trace()
    # 验证code 
    def validate_code(self, code):
        # 用户注册，以post方式提交信息，post的数据都存储在initial_data 里面
        # username 就是用户注册的手机号码, 验证码需要按照时间倒序排序，为后面验证过期，错误
        
        # 获取前端输入的username 根据表中的电话号码查询数据 再
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')


        if verify_records:
            # 最近的一个验证码
            last_record = verify_records[0]
            # 有效期为五分钟。
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            # 修改时间格式
            # import ipdb; ipdb.set_trace()
            # record_time = record_time.strftime("%Y-%m-%d %H:%M:%S")
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

        # 所有字段。attrs是字段验证合法之后返回的总的dict
    def validate(self, attrs):
        # import ipdb; ipdb.set_trace()
        #前端没有传mobile值到后端，这里添加进来
        attrs["mobile"] = attrs["username"]
        # code是自己添加得，数据库中并没有这个字段，验证完就删除掉
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ('username','code','mobile', 'password')

    # 输入密码的时候不显示明文
    password = serializers.CharField(
        style={'input_type': 'password'}, label="密码", write_only=True
    )

    # 密码加密保存
    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详细信息"""
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")
        


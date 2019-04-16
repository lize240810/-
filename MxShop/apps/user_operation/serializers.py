from rest_framework import serializers
from user_operation.models import UserFav, UserLeavingMessage
from rest_framework.validators import UniqueTogetherValidator
from goods.serializers import GoodsSerializer

class UserFavSerializers(serializers.ModelSerializer):
    """收藏序列化 用于收藏商品时"""
    user = serializers.HiddenField(  # 隐藏字段
        default=serializers.CurrentUserDefault()  # 默认当前用户
    )
    # goods = GoodsSerializer() # 嵌套显示
    class Meta:
        # 实现唯一联合， 一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),  # 结果集
                fields=('user', 'goods'),  # 指定字段
                message="已经收藏"
            )
        ]
        model = UserFav
        # 收藏的时候需要返回商品id 因为取消收藏的时候需要使用商品id
        fields = ('user', 'goods', 'id')


class UserFavDetailSerializer(serializers.ModelSerializer):
    """用户收藏详细 用于商品展示时"""
    # 用过商品Id获取收藏的商品, 需要前台的商品的序列化
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ("goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    """用户留言"""
    # 获取当前登录用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault() # 默认当前用户
    )
    # read_only 只返回 post时候可以不用提交, format格式化输出
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id" ,"add_time")

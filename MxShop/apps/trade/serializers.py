import random
import datetime
import time

from rest_framework import serializers
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import Goods
from goods.serializers import GoodsSerializer
from MxShop.settings import ali_pub_key_path, private_key_path
from utils.alipay import AliPay


class ShopSerializer(serializers.Serializer):
    """添加商品购物车"""
    '''
        继承 Serializer必须制定queryset对象， 
        继承 ModelsSerializer 则不需要指定
    '''
    # 获取当前登录用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault() 
    )
    nums = serializers.IntegerField(
        required=True, label="数量", min_value=1,
        error_messages={
            "min_value": "商品数量不能小于1",
            "required": "请选择够买的数量"
        }
    )
    # goods是一个外键 通过这个方法可以获取到goods中所有的值
    # goods = serializers.PrimaryKeyRelatedField(required=True)
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())


    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']
        # 根据商品查询购物车中是否存在
        # import ipdb; ipdb.set_trace()
        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        # 如果存在就数量+1
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            # 不存在就创建
            existed = ShoppingCart.objects.create(**validated_data)
        return existed


    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance

class ShopCartDetailSerializer(serializers.ModelSerializer):
    '''
    购物车商品详情信息
    '''
    # 一个购物车对应一个商品
    goods = GoodsSerializer(many=False, read_only=True)
    class Meta:
        model = ShoppingCart
        fields = ("goods", "nums")


# -----------------------订单管理---------------------
class OrderGoodsSerializer(serializers.ModelSerializer):
    """订单商品"""
    goods = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = "__all__"

# 订单商品相信信息
class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """订单"""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 生成订单不用post
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    nonce_st = serializers.CharField(read_only=True)
    pay_type = serializers.CharField(read_only=True)
    # 支付订单的url
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016092600599306",
            app_notify_url="http://47.98.34.221:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.98.34.221:8000/alipay/return/"
        )

        # import ipdb;ipdb.set_trace()
        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_money,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url


    def generate_order_sn(self):
        # 生成订单号 当前时间加当前用户id 加随机数
        random_ins = random.Random()
        order_sn = "{time_str}{userid}{ranstr}".format(
                time_str=time.strftime("%Y%m%d%H%M%S"), # 获取时间
                userid=self.context['request'].user.id,
                ranstr=random_ins.randint(10,99)) # 10-99的两位数随机数
        return order_sn

    def validate(self, attrs):
        # 验证码
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"

# -------------支付宝支付------------------

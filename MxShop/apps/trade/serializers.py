from rest_framework import serializers

from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import Goods
from goods.serializers import GoodsSerializer

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
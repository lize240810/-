from rest_framework import serializers
from goods.models import Goods, GoodsCategory, GoodsImage


# class GoodsSerializer(serializers.Serializer):
# 	"""Serializer实现商品展示"""
# 	name = serializers.CharField(required=True, max_length=100)
# 	click_num = serializers.IntegerField(default=0)
# 	goods_front_image = serializers.ImageField()

class CategorySerializer_three(serializers.ModelSerializer):
    """三级分类"""
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer_two(serializers.ModelSerializer):
    """二级分类"""
    sub_cat = CategorySerializer_three(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer_one(serializers.ModelSerializer):
    """一级分类"""
    sub_cat = CategorySerializer_two(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


# 商品轮播图
class GoodsImageSerializer(serializers.Serializer):
    """商品轮播图"""
    class Meta:
        model = GoodsImage  # 指定模型
        fields = ('images', )  # 需要显示的字段


# ModelSerizlizer 实现商品列表页
class GoodsSerializer(serializers.ModelSerializer):
    """覆盖外键字段"""
    # 这里使用了serializer的嵌套功能 可以详细的显示分类的信息
    category = CategorySerializer_three()
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = '__all__'

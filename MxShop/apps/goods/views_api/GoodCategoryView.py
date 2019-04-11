# 商品类别
from rest_framework import (
    mixins,  
    generics, # generics 继承了APIView 封装的方法更多
    viewsets
    )
from goods.models import GoodsCategory
from goods.serializers import CategorySerializer_one

class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""商品分类"""
	# import ipdb; ipdb.set_trace()
	queryset = GoodsCategory.objects.filter(category_type=1)
	# 序列化
	serializer_class = CategorySerializer_one
	# 想要获取某一个商品内容 继承 mixins.RetrieveModelMixin就可以


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    mixins,  
    generics,
    # generics 继承了APIView 封装的方法更多
    viewsets
    )

from goods.serializers import GoodsSerializer
from goods.paging import GoodsPagination
from goods.filters import GoodsFilter
from goods.models import Goods
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# 一.单一使用 APIView
# class GoodsListView(APIView):
#   """商品列表"""
#   def get(self, request, format=None):
#       goods = Goods.objects.all()
#       # import ipdb; ipdb.set_trace()
#       goods_serializer = GoodsSerializer(goods, many=True)
#       return Response(goods_serializer.data)

# 二. 加入使用 GenericView 
# class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
#     """商品展示页"""
#     # 1. 获取商品信息 只有三行代码
#     # 2. 添加配置 加入分页功能
#     # 查询全部数据
#     queryset = Goods.objects.all()
#     pagination_class = GoodsPagination
#     # 序列化使用模块
#     serializer_class = GoodsSerializer
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


# 三。 使用ViewSet 
class GoodsListViewSet(
    mixins.ListModelMixin, # ListModelMixin 里面list方法帮我们做好了分页和序列化的工作，只要调用就好了
    mixins.RetrieveModelMixin, #要想获取某一个商品的详情的时候，继承 mixins.RetrieveModelMixin  就可以了
    viewsets.GenericViewSet): # GenericAPIView继承APIView，封装了很多方法，比APIView功能更强大
    """
        list: 商品列表， 分页，搜索， 过滤， 排序
        retrieve: 获取商品详细信息
    """
    '''
        mixins 主要是作用于 局部增删改查 get与商品关联， 分页等
    '''
    # 这里必须要定义一个默认排序
    queryset = Goods.objects.all().order_by('id')
    # 分页
    pagination_class = GoodsPagination
    # 序列化
    serializer_class = GoodsSerializer
    
    # 把功能显示到过滤器中
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    
    # 设置filter的类为我们自定义的类
    #过滤
    filter_class = GoodsFilter
    #搜索,=name表示精确搜索，也可以使用各种正则表达式
    search_fields = ('=name','goods_brief')
    #排序
    ordering_fields = ('sold_num', 'add_time')
    ordering_fields = ('sold_num', 'add_time')
        
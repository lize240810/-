import json

from django.views.generic import View
from goods.models import Goods
from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict # 返回某个模型的字典类型
from django.core import serializers


class GoodsListView(View):
	"""商品列表
		
	"""
	def get(self, request):

		# 通过django的view实现商品列表页
		# 获取所有商品
		goods = Goods.objects.all()
		good_list = []
		# 一。 字段单个提取，返回json格式数据
		# for good in goods:
		# 	good_dict = {}
		# 	good_dict['name'] = good.name
		# 	good_dict['category'] = good.category.name
		# 	good_dict['market_price'] = good.market_price
		# 	good_list.append(good_dict)
		# return HttpResponse(json.dumps(good_list))

		# 二。 直接提取模型 
		# for good in goods:
		# 	good_dict = model_to_dict(good)
		# 	good_list.append(good_dict)
		# return HttpResponse(good_list)
		# 出现 其他类型的 会抛出异常

		# 三。 使用django的序列化
		good_data = serializers.serialize('json', goods)
		# import ipdb; ipdb.set_trace()
		good_list = json.loads(good_data)
		return JsonResponse(good_list, safe=False)


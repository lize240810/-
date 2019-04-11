'''
	自定义分页
'''
from rest_framework.pagination import PageNumberPagination


class GoodsPagination(PageNumberPagination):
	"""商品自定义分页"""
	# 默认分页模块
	page_size = 10
	# 可以动态修改每页显示个数
	page_size_query_param = 'page_size'
	# 页码参数
	page_query_param = 'page'
	# 最多显示多少页
	max_page_size = 100


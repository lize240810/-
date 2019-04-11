# import ipdb; ipdb.set_trace()
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class CustomBackend(ModelBackend):
	"""
		自定义用户验证
	"""
	def authenticate(self, username=None, password=None, **kwargs):
		try:
			# 用户名和手机 邮箱 都可以登录 
			user = User.objects.get(
				Q(username=username) | Q(mobile=username) |
				Q(email=username)
			)
			# 判断密码
			if user.check_password(password):
				# 返回用户
				return user
		except Exception as e:
			return None

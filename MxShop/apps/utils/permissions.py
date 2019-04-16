# drf权限认证
from rest_framework import permissions


class IsOwerOrReadOnly(permissions.BasePermission):
	"""自定义权限认证"""
	def has_objects_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True

		# obj相当于数据的model
		return obj.user == request.user


from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from user_operation.view.UserViews import UserFavViewset, LeavingMessageViewset, AddressSerializers

router = DefaultRouter()
# 注册路由
router.register(r'userfavs', UserFavViewset, base_name="userfavs")
router.register(r'leavingmessage', LeavingMessageViewset, base_name="leavingmessage")
router.register(r'address', AddressSerializers, base_name="address")



urlpatterns = [
	re_path(r'^', include(router.urls)),
]
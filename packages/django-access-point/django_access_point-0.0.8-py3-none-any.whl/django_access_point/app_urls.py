from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PlatformUserList, PlatformUserCustomField

router = DefaultRouter()
router.register(r'custom-fields/platform/users', PlatformUserCustomField, basename='platform.user.custom_fields')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login', ""),
    path('platform/users', PlatformUserList.as_view(), name='platform.user.list'), # platform user list
    path('platform/users/<user_id>', ""),
    path('platform/users', ""),
    path('platform/users/<user_id>', ""),
    path('platform/users/<user_id>', ""),
    path('platform/tenants', ""),
    path('tenant/users', ""), # tenant user list - tenant users mapped to logged-in user's tenant
    path('tenant/<tenant_id>/users', ""), # tenant user list - tenant users mapped to tenant_id
    path('tenant/users/<user_id>', ""),
    path('tenant/users', ""),
    path('tenant/users/<user_id>', ""),
    path('tenant/users/<user_id>', ""),
]

urlpatterns += router.urls
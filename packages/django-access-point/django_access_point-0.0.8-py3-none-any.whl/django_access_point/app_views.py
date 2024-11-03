from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from django_access_point.models.user import USER_TYPE_CHOICES, USER_STATUS_CHOICES
from django_access_point.models.custom_field import CUSTOM_FIELD_STATUS
from django_access_point.views.custom_field import CustomFieldViewSet

from .models import User, UserCustomField
from .serializers import UserSerializer, UserCustomFieldSerializer
from .filters import UserSearchFilter

class PlatformUserList(generics.ListAPIView):
    queryset = User.objects.filter(user_type=USER_TYPE_CHOICES[0][0]).exclude(status=USER_STATUS_CHOICES[0][0])
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserSearchFilter

class PlatformUserCustomField(CustomFieldViewSet):
    queryset = UserCustomField.objects.filter(user_type=USER_TYPE_CHOICES[0][0], status=CUSTOM_FIELD_STATUS[1][0])
    serializer_class = UserCustomFieldSerializer

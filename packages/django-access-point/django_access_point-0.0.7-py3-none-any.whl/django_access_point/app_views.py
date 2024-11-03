from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from django_access_point.models.user import USER_TYPE_CHOICES, USER_STATUS_CHOICES

from .models import User
from .serializers import UserSerializer
from .filters import UserSearchFilter

class PlatformUserList(generics.ListAPIView):
    queryset = User.objects.filter(user_type=USER_TYPE_CHOICES[0][0]).exclude(status=USER_STATUS_CHOICES[0][0]).all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserSearchFilter

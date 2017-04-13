from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.layers.models import TelegramPhoto
from .serializers import TelegramPhotoSerializer
from .pagination import LimitOffsetPagination


class TelegramPhotoViewSet(ReadOnlyModelViewSet):
    serializer_class = TelegramPhotoSerializer
    queryset = TelegramPhoto.objects.all()
    pagination_class = LimitOffsetPagination

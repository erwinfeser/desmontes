from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.layers.models import TelegramPhoto
from .serializers import LayerSerializer
from .pagination import LimitOffsetPagination


class TelegramPhotoViewSet(ReadOnlyModelViewSet):
    serializer_class = LayerSerializer
    queryset = TelegramPhoto.objects.all()
    pagination_class = LimitOffsetPagination

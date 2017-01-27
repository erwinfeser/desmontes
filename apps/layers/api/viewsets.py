from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters import (
    FilterSet,
    CharFilter,
    OrderingFilter
)
from apps.layers.models import Layer
from .serializers import LayerSerializer
from .pagination import LimitOffsetPagination


class LayerFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains')
    ordering = OrderingFilter(
        fields=(
            'title',
            'created',
            'updated'
        )
    )

    class Meta:
        model = Layer
        fields = [
            'title',
            'created',
            'updated',
            'ordering'
        ]


class LayerViewSet(ReadOnlyModelViewSet):
    serializer_class = LayerSerializer
    queryset = Layer.objects.all()
    filter_class = LayerFilter
    pagination_class = LimitOffsetPagination

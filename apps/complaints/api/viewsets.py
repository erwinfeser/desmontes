from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters import (
    FilterSet,
    CharFilter,
    OrderingFilter
)
from apps.complaints.models import Complaint
from .serializers import ComplaintSerializer
from .pagination import LimitOffsetPagination


class ComplaintFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains')
    ordering = OrderingFilter(
        fields=(
            'title',
            'created',
            'updated'
        )
    )

    class Meta:
        model = Complaint
        fields = [
            'title',
            'created',
            'updated',
            'ordering'
        ]


class ComplaintViewSet(ReadOnlyModelViewSet):
    serializer_class = ComplaintSerializer
    queryset = Complaint.objects.all()
    filter_class = ComplaintFilter
    pagination_class = LimitOffsetPagination

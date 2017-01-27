from rest_framework.pagination import LimitOffsetPagination as Pagination


class LimitOffsetPagination(Pagination):
    default_limit = 25
    max_limit = 250

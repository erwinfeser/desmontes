from rest_framework.routers import SimpleRouter
from .viewsets import (
    LayerViewSet
)

router = SimpleRouter(trailing_slash=False)

router.register('layers', LayerViewSet)

urlpatterns = router.urls

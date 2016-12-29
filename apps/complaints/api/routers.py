from rest_framework.routers import SimpleRouter
from .viewsets import (
    ComplaintViewSet
)

router = SimpleRouter(trailing_slash=False)

router.register('complaints', ComplaintViewSet)

urlpatterns = router.urls

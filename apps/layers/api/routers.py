from rest_framework.routers import SimpleRouter
from .viewsets import (
    TelegramPhotoViewSet
)

router = SimpleRouter(trailing_slash=False)

router.register('telegram-photos', TelegramPhotoViewSet)

urlpatterns = router.urls

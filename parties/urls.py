"""Routes for the parties feature, mounted under /api/."""
from rest_framework.routers import DefaultRouter

from .views import PartyViewSet

router = DefaultRouter()
router.register("parties", PartyViewSet, basename="party")

urlpatterns = router.urls

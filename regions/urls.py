from rest_framework import routers

from regions.views import RegionView


router = routers.SimpleRouter()
router.register(r'regions', RegionView)
urlpatterns = router.urls

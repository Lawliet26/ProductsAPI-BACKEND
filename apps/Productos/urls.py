from rest_framework.routers import SimpleRouter
from .views import ProductoView

router=SimpleRouter(trailing_slash=True)
router.register("productos", ProductoView)

urlpatterns = router.urls
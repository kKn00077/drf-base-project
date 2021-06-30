from django.urls import path, include

from rest_framework import routers
from apps.files.views import FileViewset

router = routers.SimpleRouter()
router.register(r"file", FileViewset)

urlpatterns = [
    path("", include(router.urls)),
]

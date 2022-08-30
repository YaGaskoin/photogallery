from rest_framework import routers
from gallery.views import *
from user.views import *


router = routers.SimpleRouter()
router.register(r'image', ImageViewSet, basename='image')

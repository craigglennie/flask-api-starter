from my_app.v2014_01_19.views import api
from tests.base import ResourceTestCase

class ResourceTestCase(ResourceTestCase):
    RESOURCE = None

    def setUp(self):
        super(ResourceTestCase, self).setUp(api, self.RESOURCE)


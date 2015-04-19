from rest_framework import viewsets

from webservice.tests.mock_webservice.serializers import SynchronizedModelSerializer, PlainI18NModelSerializer
from webservice.tests.mock_webservice import models
from webservice.views import delta_update


@delta_update
class StubSynchronizedModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.SynchronizedModel.objects.all()
    serializer_class = SynchronizedModelSerializer
    permission_classes = ()
    authentication_classes = ()
    lookup_field = 'uuid'


class StubI18NModelViewSet(viewsets.ModelViewSet):
    queryset = models.I18N.objects.all()
    serializer_class = PlainI18NModelSerializer
    permission_classes = ()
    authentication_classes = ()
    lookup_field = 'uuid'
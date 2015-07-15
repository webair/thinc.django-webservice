from rest_framework import serializers

from webservice.tests.mock_webservice import models
from webservice.serializers import I18NModelSerializer, SYNCHRONIZED_MODEL_FIELDS, synchronized

@synchronized
class SynchronizedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Synchronized
        fields = ('test_title', )


class PlainI18NModelSerializer(I18NModelSerializer):
    class Meta:
        model = models.I18N
        fields = SYNCHRONIZED_MODEL_FIELDS + ("uuid", "title")
        i18n_fields = ('content_title', )
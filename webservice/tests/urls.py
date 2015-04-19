from django.conf.urls import patterns, url, include
from rest_framework import routers

from webservice.tests.mock_webservice.views import StubSynchronizedModelViewSet, StubI18NModelViewSet


router = routers.DefaultRouter()
router.register(r'SynchronizedViewSet', StubSynchronizedModelViewSet)
router.register(r'I18nViewSet', StubI18NModelViewSet)

urlpatterns = patterns('',
                       url(r'', include(router.urls))
                       )
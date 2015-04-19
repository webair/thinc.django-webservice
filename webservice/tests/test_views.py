import json
from email.utils import format_datetime
from datetime import timedelta

from rest_framework.test import APIClient
from django.test import TestCase
from webservice.tests.mock_webservice.models import SynchronizedModel


class TestDeltaUpdateDecorator(TestCase):
    urls = 'webservice.tests.urls'

    def setUp(self):
        self.deleted_model = SynchronizedModel(test_title="deleted",
                                               status=SynchronizedModel.STATUS_PUBLISHED_DELETED)
        self.deleted_model.save()
        self.published_model = SynchronizedModel(test_title="published",
                                                 status=SynchronizedModel.STATUS_PUBLISHED)
        self.published_model.save()
        self.published_deleted_model = SynchronizedModel(test_title="published deleted",
                                                         status=SynchronizedModel.STATUS_PUBLISHED_DRAFT)
        self.published_deleted_model.save()
        self.draft_model = SynchronizedModel(test_title="draft",
                                             status=SynchronizedModel.STATUS_DRAFT)
        self.draft_model.save()

    def test_initial_request(self):
        client = APIClient()
        response = client.get('/SynchronizedViewSet/')
        content = json.loads(response.content.decode())
        self.assertEquals(1, len(content))
        self.assertEquals(self.published_model.test_title, content[0]["test_title"])

    def test_not_modified(self):
        client = APIClient()
        update_since_header = format_datetime(self.draft_model.updated + timedelta(seconds=10))
        response = client.get('/SynchronizedViewSet/', None, **{"HTTP_IF_MODIFIED_SINCE": update_since_header})
        self.assertEquals(304, response.status_code)
        self.assertEquals("", response.content.decode())

    def test_delta_modified(self):
        client = APIClient()
        update_since_header = format_datetime(self.draft_model.updated - timedelta(seconds=10))
        response = client.get('/SynchronizedViewSet/', None, **{"HTTP_IF_MODIFIED_SINCE": update_since_header})
        content = json.loads(response.content.decode())
        self.assertEquals(3, len(content))
        expected_titles = ["deleted", "published", "published deleted"]
        titles = []
        for o in content:
            titles.append(o["test_title"])
        self.assertListEqual(expected_titles, titles)
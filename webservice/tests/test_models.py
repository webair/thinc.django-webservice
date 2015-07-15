from django.conf import settings
from django.test import TestCase
from webservice.models import SynchronizedModel

from webservice.tests.mock_webservice.models import Synchronized, I18N, I18NContent


class TestSynchronizedModel(TestCase):
    def test_create_and_update(self):
        tm = Synchronized()
        self.assertIsNone(tm.created, "not created yet")
        self.assertIsNone(tm.updated, "not updated yet")
        tm.save()
        self.assertIsNotNone(tm.created, "created is set now")
        self.assertIsNotNone(tm.updated, "updated is set now")
        created = tm.created
        updated = tm.updated
        tm.title = "Test Changed"
        tm.save()
        self.assertEqual(tm.created, created, "created should not change")
        self.assertNotEqual(tm.updated, updated, "updated should be changed")

    def test_delete_draft(self):
        tm = Synchronized()
        tm.save()
        pk = tm.pk
        tm.delete()
        self.assertIsNone(tm.pk)
        self.assertEqual(0, Synchronized.objects.filter(pk=pk).count())

    def test_delete_published(self):
        tm = Synchronized(status=SynchronizedModel.STATUS_PUBLISHED)
        tm.save()
        tm.delete()
        self.assertIsNotNone(tm.pk)
        tm = Synchronized.objects.get(pk=tm.pk)
        self.assertEqual(SynchronizedModel.STATUS_PUBLISHED_DELETED, tm.status)

    def test_bulk_delete_draft(self):
        # test bulk deletion
        tm = Synchronized(test_title="model1")
        tm.save()
        pk = tm.pk
        Synchronized.objects.filter(test_title="model1").delete()
        self.assertEqual(0, Synchronized.objects.filter(pk=pk).count())

    def test_bulk_delete_published(self):
        # test bulk deletion
        tm = Synchronized(test_title="model1", status=SynchronizedModel.STATUS_PUBLISHED)
        tm.save()
        Synchronized.objects.filter(test_title="model1").delete()
        self.assertIsNotNone(tm.pk)
        tm = Synchronized.objects.get(pk=tm.pk)
        self.assertEqual(SynchronizedModel.STATUS_PUBLISHED_DELETED, tm.status)

    def test_is_deleted(self):
        # test bulk deletion
        tm = Synchronized(test_title="model1", status=SynchronizedModel.STATUS_PUBLISHED)
        self.assertFalse(tm.is_deleted)
        tm = Synchronized(test_title="model1", status=SynchronizedModel.STATUS_PUBLISHED_DELETED)
        self.assertTrue(tm.is_deleted)
        tm = Synchronized(test_title="model1", status=SynchronizedModel.STATUS_PUBLISHED_DRAFT)
        self.assertTrue(tm.is_deleted)



class TestI18NModel(TestCase):
    def test_default_language(self):
        main = I18N(title="data_model")
        main.save()
        content = I18NContent(content_title="test", base_model=main)
        self.assertEqual(settings.LANGUAGES[0][0], content.language)

    def test_update_timestamp(self):
        main = I18N(title="data_model")
        main.save()
        content = I18NContent(content_title="test", base_model=main)
        content.save()
        updated = main.updated
        content.test_title = "new title"
        content.save()
        self.assertLess(updated, main.updated)
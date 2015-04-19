from django.conf import settings
from django.test import TestCase

from webservice.tests.mock_webservice.models import SynchronizedModel, I18N, I18NContent


class TestSynchronizedModel(TestCase):
    def test_create_and_update(self):
        tm = SynchronizedModel()
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
        tm = SynchronizedModel()
        tm.save()
        pk = tm.pk
        tm.delete()
        self.assertIsNone(tm.pk)
        self.assertEqual(0, SynchronizedModel.objects.filter(pk=pk).count())

    def test_delete_published(self):
        tm = SynchronizedModel(status=SynchronizedModel.STATUS_PUBLISHED)
        tm.save()
        tm.delete()
        self.assertIsNotNone(tm.pk)
        tm = SynchronizedModel.objects.get(pk=tm.pk)
        self.assertEqual(SynchronizedModel.STATUS_PUBLISHED_DELETED, tm.status)

    def test_bulk_delete_draft(self):
        # test bulk deletion
        tm = SynchronizedModel(test_title="model1")
        tm.save()
        pk = tm.pk
        SynchronizedModel.objects.filter(test_title="model1").delete()
        self.assertEqual(0, SynchronizedModel.objects.filter(pk=pk).count())

    def test_bulk_delete_published(self):
        # test bulk deletion
        tm = SynchronizedModel(test_title="model1", status=SynchronizedModel.STATUS_PUBLISHED)
        tm.save()
        SynchronizedModel.objects.filter(test_title="model1").delete()
        self.assertIsNotNone(tm.pk)
        tm = SynchronizedModel.objects.get(pk=tm.pk)
        self.assertEqual(SynchronizedModel.STATUS_PUBLISHED_DELETED, tm.status)


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
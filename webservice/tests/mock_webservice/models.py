from django.db import models

from webservice.models import SynchronizedModel, ContentModel, I18NForeignKey


class ManyToMany(models.Model):
    test_title = models.CharField(max_length=255)


class Model(models.Model):
    test_title = models.CharField(max_length=255)
    test_number = models.IntegerField(null=True)
    test_boolean = models.BooleanField(default=False)
    test_datetime = models.DateTimeField(null=True)
    test_date = models.DateField(null=True)
    test_many_to_many = models.ManyToManyField(ManyToMany)


class Foreign(models.Model):
    title = models.CharField(max_length=255)
    main = models.ForeignKey(Model)


class I18N(SynchronizedModel):
    title = models.CharField(max_length=255)


class I18NContent(ContentModel):
    base_model = I18NForeignKey(I18N)
    content_title = models.CharField(max_length=255)


class SynchronizedModel(SynchronizedModel):
    test_title = models.CharField(max_length=255, null=True, blank=True)
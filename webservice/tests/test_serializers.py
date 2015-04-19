from unittest import mock

from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from webservice.serializers import I18NModelSerializer, I18NModelField
from webservice.tests.mock_webservice.models import I18N, I18NContent


@mock.patch('rest_framework.serializers.Field.context',
            mock.PropertyMock(return_value={"request": mock.Mock(LANGUAGE_CODE="de")}))
class TestI18NModelField(TestCase):
    def test_get_attribute(self):
        mock_attribute = mock.Mock()
        mock_instance = mock.Mock()
        mock_instance.attribute = mock.Mock()
        mock_instance.attribute.get = mock.Mock(return_value=mock_attribute)
        i18n_field = I18NModelField(source="attribute.field_name")
        self.assertEqual(mock_attribute, i18n_field.get_attribute(mock_instance))
        mock_instance.attribute.get.assert_called_once_with(language="de", base_model=mock_instance)

    @mock.patch('django.conf.settings.LANGUAGES', (('en', 'label'), ('de', 'label')))
    def test_get_attribute_fallback_language(self):
        mock_attribute = mock.Mock()
        mock_instance = mock.Mock()
        mock_instance.attribute = mock.Mock()

        def side_effect(language, base_model):
            if language == "en":
                return mock_attribute
            raise ObjectDoesNotExist()

        mock_instance.attribute.get = mock.Mock(side_effect=side_effect)
        i18n_field = I18NModelField(source="attribute.field_name")
        self.assertEqual(mock_attribute, i18n_field.get_attribute(mock_instance))
        self.assertEqual(2, mock_instance.attribute.get.call_count)
        self.assertEqual(mock.call(language="de", base_model=mock_instance), mock_instance.attribute.get.call_args_list[0])
        self.assertEqual(mock.call(language="en", base_model=mock_instance), mock_instance.attribute.get.call_args_list[1])

    def test_to_representation(self):
        mock_instance = mock.Mock(field_name="field_value")
        i18n_field = I18NModelField(source="attribute.field_name")
        i18n_field.field_name = "field_name"
        self.assertEqual("field_value", i18n_field.to_representation(mock_instance))

    def test_to_representation_with_None(self):
        i18n_field = I18NModelField(source="attribute.field_name")
        i18n_field.field_name = "field_name"
        self.assertIsNone(i18n_field.to_representation(None))

    def test_to_internal(self):
        i18n_field = I18NModelField(source="attribute.field_name")
        i18n_field.field_name = "field_name"
        self.assertEqual("value", i18n_field.to_internal_value("value"))


class StubSerializer(I18NModelSerializer):
    class Meta:
        fields = ('content_title', 'title')
        model = I18N

    content_title = I18NModelField(source="contents.content_title")


class StubAutoI18nFieldSerializer(I18NModelSerializer):
    class Meta:
        fields = ('title', )
        model = I18N
        i18n_fields = ('contents.content_title', )


@mock.patch('rest_framework.serializers.ModelSerializer.context',
            mock.PropertyMock(return_value={"request": mock.Mock(LANGUAGE_CODE="de")}))
class TestI18NModelSerializer(TestCase):
    def test_i18n_fields(self):
        serializer = StubSerializer()
        self.assertEqual(serializer.fields["content_title"], serializer.i18n_fields["content_title"])

    def test_create_optional(self):
        serializer = StubSerializer()
        i18n_model = serializer.create({"title": "title_value"})
        self.assertEqual("title_value", i18n_model.title)

    def test_extract_i18n_data(self):
        data = {"title": "title_value", "contents": {"content_title": "content_title_value"}}
        serializer = StubSerializer()
        self.assertEqual({"contents": {"content_title": "content_title_value"}}, serializer.extract_i18n_content(data))

    def test_create_i18n_content(self):
        i18n_model = I18N(title="something")
        i18n_model.save()
        data = {"contents": {"content_title": "content_title_value"}}
        serializer = StubSerializer()
        serializer.update_i18n_content(i18n_model, data)
        content_model = i18n_model.contents.all()[0]
        self.assertEqual("de", content_model.language)
        self.assertEqual("content_title_value", content_model.content_title)
        self.assertEqual(1, I18NContent.objects.filter(base_model=i18n_model).count())

    def test_update_i18n_content(self):
        i18n_model = I18N(title="something")
        i18n_model.save()
        i18n_content = I18NContent(content_title="some value", base_model=i18n_model, language="de")
        i18n_content.save()
        data = {"contents": {"content_title": "content_title_value"}}
        serializer = StubSerializer()
        serializer.update_i18n_content(i18n_model, data)
        content_model = i18n_model.contents.all()[0]
        self.assertEqual("de", content_model.language)
        self.assertEqual("content_title_value", content_model.content_title)
        self.assertEqual(1, I18NContent.objects.filter(base_model=i18n_model).count())

    def test_create(self):
        serializer = StubSerializer()
        i18n_model = serializer.create({"title": "title_value", "contents": {"content_title": "content_title_value"}})
        self.assertEqual("title_value", i18n_model.title)
        self.assertEqual("content_title_value", i18n_model.contents.all()[0].content_title)

    def test_update(self):
        i18n_model = I18N(title="something")
        serializer = StubSerializer()
        i18n_model = serializer.update(i18n_model,
                                       {"title": "title_value", "contents": {"content_title": "content_title_value"}})
        self.assertEqual("title_value", i18n_model.title)
        self.assertEqual("content_title_value", i18n_model.contents.all()[0].content_title)

    def test_generate_i18n_fields(self):
        serializer = StubAutoI18nFieldSerializer()
        self.assertTrue(issubclass(serializer.fields["content_title"].__class__, I18NModelField))
        self.assertEqual(serializer.fields["content_title"].source, "contents.content_title")






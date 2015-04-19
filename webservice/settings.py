from django.conf import settings

WEBSERVICE = getattr(settings, 'WEBSERVICE', {
    'IMAGE_SERVICE_TOKEN': "demo",
    'IMAGE_SERVICE_URL': "http://127.0.0.1:5000/images/demo_project/",
    'ANONYMOUS_USERNAME': "webservice_user"
})
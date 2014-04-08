from piston.authentication import HttpBasicAuthentication
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import DeviceHandler, ContainerHandler
from api.emitters import *

auth = HttpBasicAuthentication(realm="My Realm")
ad = { 'authentication': auth }

device_resource = Resource(DeviceHandler, **ad)
container_resource = Resource(ContainerHandler, **ad)

urlpatterns = patterns('',
        url(r'Containers$', container_resource),
        url(r'Devices/(?P<path>[-\w\./\s]+)$', device_resource),
        url(r'^$', device_resource),
)

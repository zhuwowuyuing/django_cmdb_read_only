from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('cmdb.views',
        (r'AddCI/$', 'add_ci'),
)


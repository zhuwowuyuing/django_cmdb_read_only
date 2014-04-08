from django.conf.urls.defaults import *
from django.contrib.auth.views import *
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^django_cmdb/', include('django_cmdb.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
	(r'^accounts/login/', login, {'template_name': 'login.html'}),
	(r'^accounts/logout/', logout, {'template_name': 'logout.html'}),
    (r'^CMDB/', include('cmdb.urls')),
    (r'^api/', include('api.urls')),

#    (r'^(?P<ci_path>[-\w\./\s]+)$', 'cmdb.views.view_ci'),
    (r'^$', direct_to_template, {'template': 'cmdb/home.html'}),
)

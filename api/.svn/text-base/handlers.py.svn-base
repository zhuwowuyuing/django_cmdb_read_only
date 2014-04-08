from piston.handler import BaseHandler
from cmdb.models import *
from misc.cmdb_lib import prefix_slash, get_correct_class, get_schema_for_ci, user_allowed_to_view_ci
import logging
import urllib
from piston.utils import rc

class DeviceHandler(BaseHandler):

    model = ConfigurationItem

    def read(self, request, path=None):

        if not path:
            return ConfigurationItem.objects.filter(is_active=True)

        # As the path might contain %20 instead of ' ' dequote it
        # and also add in the original slash
        path = '/Devices/%s' % urllib.unquote(path)
        logging.debug('In API module, path=%s' % path)
        s = get_schema_for_ci(ci_path=path)
        try:
            initial_ci = ConfigurationItem.objects.get(path=path)
        except ConfigurationItem.DoesNotExist:
            return rc.NOT_HERE

        if initial_ci.is_container:
            ci = eval('''%s.objects.filter(path__startswith='%s')''' % ( s.class_name, path ))
            logging.debug('ci = %s' % ci)
            return ci

        else:
            ci = eval('''%s.objects.get(path__startswith='%s')''' % ( s.class_name, path ))
            if user_allowed_to_view_ci(request.user, ci):
                return ci
            else:
                return rc.FORBIDDEN



class ContainerHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = ConfigurationItem

    def read(self, request):
        return ConfigurationItem.objects.filter(is_active=True, is_container=True).exclude(path='/').order_by('path')



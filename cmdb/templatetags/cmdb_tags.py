from django import template

from cmdb.models import *

register = template.Library()

class DeviceClassNode(template.Node):
    def __init__(self, var_name='device_classes'):
        self.var_name = var_name
    def render(self, context):
        context[self.var_name] = ConfigurationItem.objects.filter(is_active=True, is_container=True)
        return ''

@register.tag(name='get_device_classes')
def get_device_classes(parser, token):
    error = False
    try:
        tag_name, _as, var_name = token.split_contents()
        if _as != 'as':
            error = True
    except:
        error = True
    
    if error:
        raise TemplateSyntaxError, '''get_device_classes must be of the form,
        "get_device_classes as <var_name>"'''
    else:
        return DeviceClassNode(var_name)

class CIListNode(template.Node):
    def __init__(self, var_name='ci_list', ci=''):
        self.var_name = var_name
        self.ci = template.Variable(ci)
    def render(self, context):
        ci = self.ci.resolve(context)
        logging.debug('''ci=%s''' % ci)
        context[self.var_name] = ConfigurationItem.objects.filter(path__startswith=ci.path).exclude(path=ci.path)
        return ''

@register.tag(name='get_child_ci_list')
def get_child_ci_list(parser, token):
    error = False
    try:
        tag_name, ci, _as, var_name = token.split_contents()
        if _as != 'as':
            error = True
    except:
        error = True

    if error:
        raise TemplateSyntaxError, '''get_child_ci_list must be of the form,
        "get_child_ci_list ci as <var_name>"'''
    else:
        return CIListNode(var_name=var_name, ci=ci)

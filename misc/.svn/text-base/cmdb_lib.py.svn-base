import logging
logging.basicConfig(level=logging.DEBUG)



def get_parent_paths(path):
    """
    Return a list of strings that represents the parent classes of a ConfigurationItem.
    Running it against '/Devices/Servers/SERVER001' returns
    ['/Devices/Servers/SERVER001', '/Devices/Servers', '/Devices', '/']
    """

    split_path = path.split('/')
    try:
        split_path.remove('') # Remove the empty item that is left as the first item in the list
    except ValueError:
        # Someone has entered a path with no / in it... 
        raise ValidationError(u'Invalid Path')

    paths = [] # Create an empty list to hold the paths
    while len(split_path) > 0:
        # For each item in the CIs path
        new_path = '' # Create an empty string to hold this path
        for part in split_path:
            new_path = '''%s/%s''' % ( new_path, part)       # Generate the path
        paths.append(new_path) # Append this path to the list
        part_to_delete = split_path[-1]
        # As we iterate through the path we need to delete the last part of
        # the path.. find it now
        split_path.remove(part_to_delete)
        # Delete the part and do it all again....
    # Insert a single slash at the beginning of the list
    paths.append('/')
    # Return something like ['/Devices/Servers/SERVER001', '/Devices/Servers', '/Devices', '/']
    return paths


def get_correct_class(*args, **kwargs):
    """
    Return a Django database object that is the correct class according to
    the path. For example object /Devices/Servers/SERVER001 is a ConfigurationItem,
    Device and a Server.

    get_correct_class return the Server representation of this object

    >>> ci = ConfigurationItem.objects.get(path='/Devices/Servers/SERVER01')
    >>> get_correct_class(ci=ci)
    <Server: /Devices/Servers/SERVER01>

    You can also provide a string to get the correct object back

    >>> get_correct_class(ci_path='/Devices/Servers/SERVER01')
    <Server: /Devices/Servers/SERVER01>
    """

    from cmdb.models import *
    if not kwargs.has_key('ci'):
        ci = ConfigurationItem.objects.get(path=kwargs['ci_path'])
    else:
        ci = kwargs['ci']

    for part in get_parent_paths(ci.path):
        try:
            s = Schema.objects.get(path=part)
            # Return an object list <Server: /Devices/Servers/SERVER01>
            return eval('''%s.objects.get(path='%s')''' % ( s.class_name, ci.path))
        except Schema.DoesNotExist:
            pass
    return False

def get_schema_for_ci(*args, **kwargs):
    """
    Return the Schema object given either an instance
    of a Django object or a string containing a path

    >>> ci = ConfigurationItem.objects.get(path='/Devices/Servers/SERVER01')
    >>> get_schema_for_ci(ci=ci)
    <Schema: /Devices/Servers>

    >>> get_schema_for_ci(ci_path='/Devices/Servers/SERVER01')
    <Schema: /Devices/Servers>
    """

    from cmdb.models import ConfigurationItem, Schema
    # TODO: Get some caching happening here....
    if not kwargs.has_key('ci_path'):
        ci_path = kwargs['ci'].path
    else:
        ci_path = kwargs['ci_path']

    for part in get_parent_paths(ci_path):
        try:
            s = Schema.objects.get(path=part)
            # Return something like <Schema: /Devices/Servers>
            return s
        except Schema.DoesNotExist:
            pass
    return False
        
def prefix_slash(s):
    """
    Return a string with a path prepended to it, helpful when the URL 
    processor strips it out

    >>> prefix_slash('Devices/Servers/SERVER01')
    '/Devices/Servers/SERVER01'
    """
    return '''/%s''' % s


def collect_all_attributes_for_schema(schema):
    """
    Return a list of strings that represents the attributes associated with a Schema

    >>> s = Schema.objects.get(path='/Devices/Servers')
    >>> collect_all_attributes_for_schema(s)
    ['id', 'path', 'name', 'description', 'is_active'..... ]
    """

    from cmdb.models import *
    parent_classes = get_parent_paths(schema.path)
    fields = []
    for path in parent_classes:
        _schema = Schema.objects.get(path=path)
        instance = eval('''%s()''' % _schema.class_name)
        instance_fields = [ f.name for f in instance._meta.fields ] + \
            [ f[0].name for f in instance._meta.get_m2m_with_model() ]
        for f in instance_fields:
            if f not in fields:
                fields.append(f)
    return fields

        
def user_allowed_to_view_ci(user, ci):
    """
    Return True if a user is allowed to view a CI based on it's groups ACL.
    Return False if not
    """
    
    from cmdb.models import *
    allowed_ci_list = []
    # TODO: Get some caching going on here to avoid expensive lookups
    # For all of the users SecurityGroups....
    for s in SecurityGroup.objects.filter(id__in=[ g.id for g in user.groups.all() ]):
        for acl in s.read_acl.split('\n'):
            # TODO: Check this string for maliciousness
            logging.debug('''allowed_ci_list => %s''' % allowed_ci_list)
            allowed_ci_list += [ i['id'] for i in eval('''Device.objects.%s.filter(is_active=True).values('id')''' % acl) ]


    logging.debug('''allowed_ci_list => %s''' % allowed_ci_list)
    logging.debug('''ci.id => %s''' % ci.id)
    if ci.id in allowed_ci_list:
        return True
    else:
        return False

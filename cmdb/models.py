from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group, User
from django.utils.http import urlquote
import logging

from misc.cmdb_lib import get_parent_paths


class Schema(models.Model):

    path = models.CharField('Path', max_length=255, blank=True, unique=True)
    module_name = models.CharField('Module Name', max_length=1024, blank=True)
    class_name = models.CharField('Class', max_length=1024, blank=True)
    edit_template = models.CharField('Edit Template', max_length=1024, blank=True)
    view_template = models.CharField('View Template', max_length=1024, blank=True)
    add_template = models.CharField('Add Template', max_length=1024,  blank=True)
    form_name = models.CharField('Form Name', max_length=1024, blank=True)
    edit_form_name = models.CharField('Edit Form Name', max_length=1024, blank=True)

    def __unicode__(self):
        return u'''%s''' % self.path
                                
class ConfigurationItem(models.Model):

    path = models.CharField('Path', max_length=1024)
    name = models.CharField('Name', max_length=1024, blank=True)
    description = models.CharField('Description', max_length=1024, blank=True)
    is_active = models.BooleanField('Active', default=True)
    is_container = models.BooleanField('Is a Container Object', default=False)
    date_created = models.DateTimeField('Date Created', auto_now_add=True)
    date_modified = models.DateTimeField('Date Modified', auto_now=True)
    extension_attribute_1 = models.CharField('Extension Attribute 1', max_length=255, blank=True)
    extension_attribute_2 = models.CharField('Extension Attribute 2',max_length=255, blank=True)
    extension_attribute_3 = models.CharField('Extension Attribute 3',max_length=255, blank=True)
    extension_attribute_4 = models.CharField('Extension Attribute 4',max_length=255, blank=True)
    extension_attribute_5 = models.CharField('Extension Attribute 5',max_length=255, blank=True)
    extension_attribute_6 = models.CharField('Extension Attribute 6',max_length=255, blank=True)
    extension_attribute_7 = models.CharField('Extension Attribute 7',max_length=255, blank=True)
    extension_attribute_8 = models.CharField('Extension Attribute 8',max_length=255, blank=True)
    extension_attribute_9 = models.CharField('Extension Attribute 9',max_length=255, blank=True)
    extension_attribute_10 = models.CharField('Extension Attribute 10',max_length=255, blank=True)
    extension_attribute_11 = models.BooleanField()
    explicit_acl = models.TextField('Explicit Access Control List', blank=True)

      
    def __unicode__(self):
        return u'''%s''' % self.path

    def get_absolute_url(self):
        return u'''%s''' % urlquote(self.path)
        
    class Meta:
        ordering = ["path"]

    def save(self, *args, **kwargs):
        logging.debug("Start save function for object %s" % self.path)
        changer_name = False
        if kwargs.has_key('request'):   # Try and get the person changing the
                                        # object from the HTTP request
            try:
                changer_name = kwargs['request'] = request.user
                logging.debug("Identified user changing as %s from HTTP \
                        request" % changer_name)
            except:
                pass

        if not changer_name:
            try:    # If no request.user exists (because of admin interface
                    # we are using python commands use a dummy SYSTEM user
                changer_name = User.objects.get(username='SYSTEM')
            except:
                # TODO: Shouldn't use a example.com email address here...
                c = User.objects.create_user('SYSTEM', 'system@example.com',
                        'xxxxx')
                c.set_unusable_password()
                changer_name = c
            logging.debug("User updating object is %s" % changer_name)

        # Look at the __class__ of the object we are saving and confirm the
        # path in use is correct, else raise ValidationError
        for part in get_parent_paths(self.path):
            try:
                s = Schema.objects.get(path=part)
                logging.debug("Using schema %s" % s.path)
                break
            except:
                s = None
        if not s:
            logging.debug("No schema found for this device.")
            raise IncorrectPath, u'''No schema found for this device.'''
        logging.debug('''According to the path the class should be: %s''' % s.class_name)
        # Ensure that self.path is correct for this Model
        logging.debug('''self.class = %s''' % self.__class__)
        logging.debug('''object.class = %s''' % self.__class__)
        if self.__class__ != eval('''%s().__class__''' % s.class_name):
            raise ValidationError(u'''Incorrect path for this type of object''')
        logging.debug("Using schema %s" % s.path)

        if self.pk:
            logging.debug("Object has primary key (%s) and is ready for editing"
                    % self.pk)
            change_type = 1 # see cmdb.models.HistoryLog.LOG_UPDATE_TYPES
            change = 'CI Created'
            if s:
                
                # Ensure the objects 
                current_object = eval('''%s.objects.get(id=%s)''' % ( s.class_name, self.pk))

                changed_attributes = {}
                # Inspect the existing object and see which fields have changed.
                fields = [ f.name for f in current_object._meta.fields ]
                for f in fields:
                    if eval('''self.%s''' % f) != eval('''current_object.%s''' % f):
                        info='''Attribute "%s" changed from "%s" to "%s"''' \
                         % ( f, eval('''current_object.%s''' % f), 
                         eval('''self.%s''' % f) )
                        HistoryLog(configuration_item=self, user=changer_name, 
                         change_type=change_type,
                         info=info).save()
                        logging.debug(info)
                        # TODO: Notify the users that subscribe to this device
                        super(ConfigurationItem, self).save(*args, **kwargs)
                        return
            else:
                logging.debug("CRITICAL: No schema found for object")
                    
        else:
            change_type = 0
            logging.debug("This is a new object to add to database")
            super(ConfigurationItem, self).save(*args, **kwargs)
            HistoryLog(configuration_item=self, user=changer_name, change_type=change_type,
                info='CI Created').save()
            return
        logging.debug("Finished saving object")

class Company(ConfigurationItem):

    address = models.CharField(max_length=1024, blank=True)
    phoneNumber = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    alert_group = models.EmailField(blank=True)

class Location(ConfigurationItem):

    address = models.CharField(max_length=1024, blank=True)
    phoneNumber = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    alert_group= models.EmailField(blank=True)

class Model(ConfigurationItem):

    height = models.IntegerField('Height in U', null=True)

class Device(ConfigurationItem):

    DEPLOYMENT_STATUS = (
        ('Awaiting Decommission', 'Awaiting Decommission'),
        ('Awaiting Deployment', 'Awaiting Deployment'),
        ('Client Development', 'Client Development'),
        ('Critical', 'Critical'),
        ('Internal Development', 'Internal Development'),
        ('Production', 'Production'),
    )

    asset_tag = models.CharField('Asset Tag', max_length=255, blank=True)
    serial_number = models.CharField('Serial Number', max_length=255, blank=True)
    location = models.ForeignKey(Location, verbose_name='Location',
            related_name="devices_in_location")
    model = models.ForeignKey(Model, verbose_name='Model', blank=True,
            null=True, related_name="devices_of_type")
    machine_type = models.CharField('Machine Type', max_length=255, blank=True)
    company = models.ForeignKey(Company, verbose_name='Company',
            related_name="devices_in_company")
    ip_addresses = models.TextField('IP Address', blank=True)
    purchase_date = models.DateField('Purchase Date', blank=True, null=True)
    warranty_expire = models.DateField('Warranty Expire', blank=True, null=True)
    url = models.URLField('URL', blank=True)
    soc_number = models.CharField('PO/SOC Number', max_length=1024, blank=True)
    in_scope = models.BooleanField('Compliance In Scope', default=False)
    alert_group = models.TextField('Alert Group', blank=True)
    notify_group = models.TextField('Notify Group', blank=True)
    deployment_status = models.CharField('Deployment Status', max_length=255, blank=True, choices=DEPLOYMENT_STATUS)
    sku_number = models.CharField('SKU Number', max_length=255, blank=True)
    purchase_price = models.FloatField(blank=True, null=True)
    depreciation_period = models.IntegerField(blank=True, null=True)
    depreciation_start_date = models.DateField(blank=True, null=True)
    invoice_number = models.CharField(max_length=255, blank=True)



class OperatingSystem(ConfigurationItem):

    icon = models.ImageField(upload_to="os_icons", blank=True)
    telnet_connections = models.BooleanField()
    ssh_connections = models.BooleanField()
    http_connections = models.BooleanField()
    telnet_connections = models.BooleanField()
    rdp_connections = models.BooleanField()
    vnc_connections = models.BooleanField()

class Server(Device):

    operating_system = models.ForeignKey(OperatingSystem,
            verbose_name='Operating System', blank=True, null=True,
            related_name='servers_with_os')
    authentication_source = models.ForeignKey(ConfigurationItem,
            verbose_name='Authentication Source', blank=True, null=True,
            related_name='servers_in_authentication_source')
    patching_system = models.ForeignKey(ConfigurationItem,
            verbose_name='Patching System', blank=True, null=True,
            related_name='servers_in_patching_system')
    backup_system = models.ForeignKey(ConfigurationItem, 
            verbose_name='Backup System', blank=True, null=True,
            related_name='servers_in_backup_system')

class People(ConfigurationItem):

    first_name = models.CharField(max_length=1024)
    last_name = models.CharField(max_length=1024)
    user_principal_name = models.CharField(max_length=1024)
    email = models.CharField(max_length=1024)
    job_title = models.CharField(max_length=1024, blank=True)
    telephone_number = models.CharField(max_length=1024, blank=True)
    extension_number = models.CharField(max_length=1024, blank=True)
    company = models.ForeignKey(Company, related_name='personCompany', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    object_sid = models.CharField(max_length=1024)

class Computer(Device):

    user = models.ForeignKey(People, verbose_name='User', related_name='computerUser', blank=True, null=True)
    assigned_devices = models.ManyToManyField(Device, related_name='computerDevices', blank=True)
    mac_address = models.CharField('MAC Address', max_length=32, blank=True)

class System(ConfigurationItem):

    device_list = models.ManyToManyField(ConfigurationItem, related_name='systemDevices', blank=True)
    alert_group = models.TextField('Alert Group', blank=True)
    notify_group = models.TextField('Notify Group', blank=True)
    company = models.ForeignKey(Company, related_name='systemCompany')
    url = models.URLField(blank=True)
    dynamic_query = models.CharField('Dynamic Query String', max_length=1024, blank=True)
                
class ServiceAccount(ConfigurationItem):

    realm = models.CharField(max_length=1024)
    bind_dn = models.CharField(max_length=1024)
    bind_pw = models.CharField(max_length=1024)
    base_dn = models.CharField(max_length=1024)
    ldap_servers = models.CharField(max_length=1024)

class ADImportLocation(ConfigurationItem):

    ou = models.CharField(max_length=1024)
    credentials = models.ForeignKey(ServiceAccount, related_name='importLocationCredentials')
    company = models.ForeignKey(Company, related_name='importLocationCompany')
    exclude_group = models.CharField(max_length=255, blank=True)

class IPNetwork(ConfigurationItem):

    NETWORK_TYPES = (
        ('Internal', 'Internal'),
        ('DMZ', 'DMZ'),
        ('Storage', 'Storage'),
    )

    ip_address = models.IPAddressField()
    subnet_length = models.IntegerField()
    network_type = models.CharField(max_length=255, choices=NETWORK_TYPES)

class HistoryLog(models.Model):       

    LOG_UPDATE_TYPES = (
        (0, 'CI Creation'),
        (1, 'CI Modification'),
        (2, 'CI Decommission'),
    )

    date = models.DateTimeField(auto_now_add=True)
    configuration_item = models.ForeignKey(ConfigurationItem, related_name='deviceLog')
    user = models.ForeignKey(User)
    change_type = models.CharField(max_length=1024, choices=LOG_UPDATE_TYPES)
    info = models.CharField(max_length=1024)

    def __unicode__(self):
        return u'''%s - %s''' % ( self.configuration_item.path, self.info )

class AlertProfile(models.Model):

    user = models.ForeignKey(User, unique=True)
    alert_device_classes = models.ManyToManyField(ConfigurationItem, related_name='userAlertDeviceClass')
    alert_locations = models.ManyToManyField(Location, related_name='userAlertLocation')
    alert_email = models.BooleanField()
    alert_system = models.BooleanField()
    alert_incident = models.BooleanField()
    alert_rfc = models.BooleanField()
        
    def __str__(self):
        return '''%s Alert Profile''' % self.user.username

class SecurityGroup(Group):

    read_acl = models.TextField(blank=True)
    write_acl = models.TextField(blank=True)

import sys
import logging
logging.basicConfig(level=logging.DEBUG)

from django.core.management import setup_environ
sys.path.append('.')
import settings
setup_environ(settings)

from cmdb.models import *


logging.debug('**** Loading Initial Schema')

Schema(path='/', module_name='cmdb', class_name='ConfigurationItem',
    edit_template='cmdb/ci-edit.html', view_template='cmdb/ci-view.html',
    add_template='cmdb/ci-add.html', form_name='CIForm',
    edit_form_name='CIEditForm').save()
logging.debug('Loaded schema for /')

Schema(path='/Devices', module_name='cmdb', class_name='Device',
    edit_template='cmdb/device-edit.html', view_template='cmdb/device-view.html',
    add_template='cmdb/device-add.html', form_name='DeviceForm',
    edit_form_name='DeviceEditForm').save()
logging.debug('Loaded schema for /Devices')

Schema(path='/Devices/Servers', module_name='cmdb', class_name='Server',
    edit_template='cmdb/server-edit.html', view_template='cmdb/server-view.html',
    add_template='cmdb/server-add.html', form_name='ServerForm',
    edit_form_name='ServerEditForm').save()
logging.debug('Loaded schema for /Devices/Servers')

Schema(path='/Company', module_name='cmdb', class_name='Company',
    edit_template='cmdb/company-edit.html', view_template='cmdb/company-view.html',
    add_template='cmdb/company-add.html', form_name='CompanyForm',
    edit_form_name='CompanyEditForm').save()
logging.debug('Loaded schema for /Company')

Schema(path='/HardwareVendor', module_name='cmdb', class_name='Model',
    edit_template='cmdb/model-edit.html', view_template='cmdb/model-view.html',
    add_template='cmdb/model-add.html', form_name='HWModelForm',
    edit_form_name='HWModelEditForm').save()
logging.debug('Loaded schema for /HardwareVendor')

Schema(path='/Locations', module_name='cmdb', class_name='Location',
    edit_template='cmdb/location-edit.html', view_template='cmdb/location-view.html',
    add_template='cmdb/location-add.html', form_name='LocationForm',
    edit_form_name='LocationEditForm').save()
logging.debug('Loaded schema for /Locations')

Schema(path='/OperatingSystem', module_name='cmdb', class_name='OperatingSystem',
    edit_template='cmdb/os-edit.html', view_template='cmdb/os-view.html',
    add_template='cmdb/os-add.html', form_name='OSForm',
    edit_form_name='OSEditForm').save()
logging.debug('Loaded schema for /OperatingSystem')


logging.debug('**** Loaded Initial Schema')

logging.debug('**** Creating tree objects')
ConfigurationItem(path='/', is_container=True).save()
logging.debug('Created /')

company = Company(path='/Company', is_container=True)
company.save()
logging.debug('Created /Company')

acme = Company(path='/Company/ACME Corp')
acme.save()
logging.debug('Created /Company/ACME Corp')

anvil = Company(path='/Company/Anvil Corp')
anvil.save()
logging.debug('Created /Company/Anvil Corp')

model = Model(path='/HardwareVendor', is_container=True)
model.save()
logging.debug('Created /HardwareVendor')

hp = Model(path='/HardwareVendor/HP')
hp.save()
logging.debug('Created /HardwareVendor/HP')

location = Location(path='/Locations', is_container=True)
location.save()
logging.debug('Created /Locations')

london = Location(path='/Locations/London')
london.save()
logging.debug('Created /Locations/London')

Device(path='/Devices', location=location, model=model, company=company, is_container=True).save()
logging.debug('Created /Devices')

Device(path='/Devices/ROUTER01', company=acme, model=hp, location=london).save()
logging.debug('Created /Devices/ROUTER01')

OperatingSystem(path='/OperatingSystem', is_container=True).save()
logging.debug('Created /OperatingSystem')

linux = OperatingSystem(path='/OperatingSystem/Linux')
linux.save()
logging.debug('Created /OperatingSystem/Linux')

ConfigurationItem(path='/PatchingSystem', is_container=True).save()
logging.debug('Created /PatchingSystem')

patching_system = ConfigurationItem(path='/PatchingSystem/Default Patching System')
patching_system.save()
logging.debug('Created /PatchingSystem/Default Patching System')

ConfigurationItem(path='/AuthenticationSource', is_container=True).save()
logging.debug('Created /AuthenticationSource')

auth = ConfigurationItem(path='/AuthenticationSource/Default Authentication System')
auth.save()
logging.debug('Created /AuthenticationSource/Default Authentication Source')

ConfigurationItem(path='/BackupSystem', is_container=True).save()
logging.debug('Created /BackupSystem')

backup = ConfigurationItem(path='/BackupSystem/Default Backup System')
backup.save()
logging.debug('Created /BackupSystem/Default Backup System')

Server(path='/Devices/Servers', company=company, location=location, is_container=True).save()
logging.debug('Created /Devices/Servers')

Server(path='/Devices/Servers/SERVER01', company=acme, location=london, model=hp,
        operating_system=linux).save()
logging.debug('Created /Devices/Servers/SERVER01')

acme_user = User.objects.create_user('acme_user', 'acme_user@example.com', '1')
acme_user.save()
logging.debug('Created acme_user')

anvil_user = User.objects.create_user('anvil_user', 'anvil_user@example.com', '1')
anvil_user.save()
logging.debug('Created anvil_user')

acme_group = SecurityGroup(name='ACME_USERS')
acme_group.read_acl = '''filter(company__path__icontains='ACME')'''
acme_group.save()
logging.debug('Created ACME_USERS group')

acme_user.groups.add(acme_group)
acme_user.save()
logging.debug('Added acme_user to ACME_GROUP')

anvil_group = SecurityGroup(name='ANVIL_USERS')
anvil_group.read_acl = '''filter(company__path__icontains='Anvil')'''
anvil_group.save()
logging.debug('Created ANVIL_USERS group')

anvil_user.groups.add(anvil_group)
anvil_user.save()
logging.debug('Added anvil_user to ANVIL_GROUP')







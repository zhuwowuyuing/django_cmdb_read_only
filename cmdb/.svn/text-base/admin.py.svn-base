from cmdb.models import *
from cmdb.forms import *
from cmdb.views import decommission_ci
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

def admin_decommission_ci(modeladmin, request, queryset):
    for q in queryset:
        decommission_ci(request, ci=q)
admin_decommission_ci.short_description = 'Decommission CI'

class ConfigurationItemAdmin(admin.ModelAdmin):
    list_display = ['path', 'name', 'is_active', 'description']
    search_fields = ['path']
    actions = [admin_decommission_ci]

class DeviceAdmin(admin.ModelAdmin):
    form = DeviceForm
    list_display = ['path', 'company', 'is_active', 'description']
    search_fields = ['path', 'serial_number', 'asset_tag']
    actions = [admin_decommission_ci]
	
class ServerAdmin(admin.ModelAdmin):
    actions = [admin_decommission_ci]

admin.site.register(Schema)
admin.site.register(ConfigurationItem, ConfigurationItemAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Server, DeviceAdmin)
admin.site.register(Computer, DeviceAdmin)
admin.site.register(ServiceAccount)
admin.site.register(Location)
admin.site.register(System)
admin.site.register(Company)
admin.site.register(IPNetwork)
admin.site.register(OperatingSystem)
admin.site.register(HistoryLog)
admin.site.register(People, DeviceAdmin)
admin.site.register(ADImportLocation)
admin.site.register(SecurityGroup)



admin.site.unregister(User)

# Set it up so we can edit a user's sprockets inline in the admin
class UserProfileInline(admin.StackedInline):
    model = AlertProfile

class MyUserAdmin(UserAdmin):
    inlines = [UserProfileInline]

# re-register the User with the extended admin options
admin.site.register(User, MyUserAdmin)


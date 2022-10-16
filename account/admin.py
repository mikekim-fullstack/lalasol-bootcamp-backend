from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import *

admin.site.site_header = 'LaLaSol BootCamp Admin Site'
admin.site.site_title = 'LaLaSol BootCamp'

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name','last_name', 'is_active', 'is_superuser', 'created_date']
    list_display_links=['id', 'email',]
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'role_type']


admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(UserAccount, UserAccountAdmin)


admin.site.unregister(Group)

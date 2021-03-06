from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.

from library.models import Details
class DetailsInline(admin.StackedInline):
    model = Details
    can_delete = False
    verbose_name_plural = 'details'

class UserAdmin(BaseUserAdmin):
    inlines = (DetailsInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

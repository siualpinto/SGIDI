from django.contrib import admin

# Register your models here.


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from sgidi.models import Token


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class TokenInline(admin.StackedInline):
    model = Token
    can_delete = False
    verbose_name_plural = 'token'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (TokenInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


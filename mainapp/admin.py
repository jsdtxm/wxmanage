from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from mainapp.models import *

class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Source)
admin.site.register(QNote)
admin.site.register(Note)
admin.site.register(User_priv)
admin.site.register(Team)
admin.site.register(Sort)


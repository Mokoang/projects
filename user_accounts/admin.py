from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import user,user_permission
from .forms import upForm,userForm,changeuserForm



class upAdmin(admin.StackedInline):
    form = upForm
    model = user_permission
    extra=1
    def has_delete_permission(self, request, obj=None):
        return False

    
class userAdmin(admin.ModelAdmin):
    form = userForm
    list_display = ('user_name','First_name','Last_name', 'email','role','is_active')
    inlines = [upAdmin]

    def get_form(self, request, obj=None, **kwargs):
        if obj and obj.pk:
            return changeuserForm
        else:
            return userForm

    def has_delete_permission(self, request, obj=None):
        return False              

admin.site.unregister(User)
admin.site.register(user,userAdmin)
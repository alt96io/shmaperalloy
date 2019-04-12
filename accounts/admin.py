from django.contrib import admin
#from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import MemberCreationForm, MemberChangeForm
from .models import Member, Profile

#Member = get_user_model()

#class MemberAdmin(admin.ModelAdmin):
class MemberAdmin(BaseUserAdmin):

    form = MemberChangeForm
    add_form = MemberCreationForm

#    class Meta:
#        model = Member

    list_display = ('email', 'staff', 'admin')
    list_filter = ('admin', 'staff', 'active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'staff', 'active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
    )
    search_fields = ['email']
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(Member, MemberAdmin)
admin.site.register(Profile)


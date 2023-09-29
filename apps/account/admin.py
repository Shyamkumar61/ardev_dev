from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
from .forms import SingUpForm
# Register your models here.


class AccountAdmin(UserAdmin):
    model = Account
    add_form = SingUpForm
    search_fields = ('email',)
    list_filter = ('email', 'username', 'is_staff')
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    # ordering = ('-data_joined',)


admin.site.register(Account, AccountAdmin)

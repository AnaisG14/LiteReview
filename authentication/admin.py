from django.contrib import admin
from .forms import UserForm
from .models import User


# register UserAdmin to authorize modification of password
class UserAdmin(admin.ModelAdmin):
    form = UserForm

    list_filter = ('username',)


admin.site.register(User, UserAdmin)

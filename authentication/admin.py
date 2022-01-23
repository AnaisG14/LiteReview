from django.contrib import admin
from authentication.models import User

# register the new admin of the site
admin.site.register(User)

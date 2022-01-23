from django.contrib import admin
from review.models import Ticket, Review, UserFollows

# admin db on browser
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)

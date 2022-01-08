from django.contrib.auth.models import AbstractUser
from django.db import models

from review.models import UserFollows


class User(AbstractUser):
    pass




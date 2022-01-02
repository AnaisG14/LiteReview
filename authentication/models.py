from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follower = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name='suit',
    )



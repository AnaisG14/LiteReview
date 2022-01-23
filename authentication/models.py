from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
     A class used to represent a User. inherited of AbstractUser Class.
    ...

    Attributes inherited of AbstractUser and used in this application
    ----------
    username : str
        A string to define a username of the user.
    first_name : str
        The first name of the user.
    last_name : str
        The last name of the user.
    email : str
        The email address of the user.
    password :
        The password of the user.

    """

    pass

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from PIL import Image


class Ticket(models.Model):
    """
    A class used to represent a Ticket
       ...

    Attributes :
       ----------
        title : str
            a string to print the title of the ticket.
        description : str
            the description of the ticket.
        user : foreign key
            a link to the author of the ticket.
        image : imageField
            the image corresponding to the ticket.
        time_created : date_time
            the date and time of the ticket creation.
        number_reviews : int
            the number of reviews for a ticket.

    Methods
       -------
        resize_image()
           Resize the image in a max size 300 * 300.
        get_review()
            Return a list of all the reviews for the ticket as a property.
            review_users can be used as an attribute.
    """

    title = models.CharField('Titre', max_length=128)
    description = models.TextField(max_length=2048)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    number_reviews = models.IntegerField(default=0)
    IMAGE_MAX_SIZE = (300, 300)

    def __str__(self):
        return f"'{self.title}' by {self.user} (id={self.id})"

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()

    @property
    def get_review(self):
        reviews = self.review_set.all()
        review_users = [review.user for review in reviews]
        return review_users


class Review(models.Model):
    """
    A class used to represent a Review.
       ...

    Attributes :
       ----------
        ticket : foreign key
            a link to the corresponding ticket
        rating : int
            the rating of the review.
        user : foreign key
            a link to the author of the review.
        headline : str
            the headline of the review.
        time_created : date_time
            the date and time of the review creation.
        body : str
            the body of the review.

    Methods :
       -------
       get_rating_star()
            Return a string to print the rating with stars and not with int.
            get_rating_star can be used as an attribute.
       """

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        'note',
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField('titre', max_length=128)
    body = models.TextField('Votre avis', max_length=8192)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"En réponse à '{self.ticket.title}' : {self.headline} par {self.user} (id={self.id})"

    @property  # instance.get_rating_star
    def get_rating_star(self):
        return chr(9733) * self.rating + chr(9734) * (5 - self.rating)


class UserFollows(models.Model):
    """
        Stores a relation between a user and its followers, related to :model:`auth.User`.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following")  # connected user
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by")   # user followed by the connected user

    class Meta:
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f"{self.user} suivi par {self.followed_user} (id={self.id})"

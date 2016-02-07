from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# This code is triggered whenever a new user has been created and saved to the database

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def user_directory_path(instance, filename):
    # image will be uploaded to MEDIA_ROOT/<id>/<filename>
    return '{0}/{1}'.format(instance.user.id, filename)

class Picture(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=False, related_name='pictures')
    image = models.ImageField(upload_to=user_directory_path)
    average_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def calc_average_rate(self):
        picture_rates = PictureRate.objects.filter(picture=self)
        count = picture_rates.count()
        total = 0
        for rate in picture_rates:
            total += rate.rate 
        self.average_rate = total / count

    class Meta:
        ordering = ('created',)

class PictureRate(models.Model):
    picture = models.ForeignKey(Picture, null=False)
    user = models.ForeignKey(User, null=False)
    rate = models.PositiveSmallIntegerField(null=False)

    class Meta:
        unique_together = ('picture', 'user')
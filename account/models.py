from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Profile(models.Model):
    # the model for the basic user

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    slug = models.SlugField(blank=True)

    profile_picture = models.ImageField(upload_to='images/profile_pictures/',
                                        default='images/profile_pictures/no_img.png')

    profile_description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)



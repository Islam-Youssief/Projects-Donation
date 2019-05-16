# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name_regex = RegexValidator(regex=r'^([A-Za-z])+$',
                                message="Please enter a valid name")

    first_name = models.CharField(max_length=30, validators=[name_regex])
    last_name = models.CharField(max_length=30, validators=[name_regex])

    email_regex = RegexValidator(regex=r'^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$',
                                 message="Please enter a valid email address")
    email = models.EmailField(
        max_length=254, unique=True, validators=[email_regex])

    image = models.ImageField(upload_to='images/user_profile/',
                              default='images/defaultUser.png')
    country = models.CharField(
        max_length=30, null=True, blank=True, validators=[name_regex])

    birthdate = models.DateTimeField(null=True, blank=True)

    phone_regex = RegexValidator(regex=r'^01[5|1|2|0][0-9]{8}$',
                                 message="Please enter a valid phone number")
    phone = models.CharField(max_length=11, validators=[
        phone_regex], null=True, blank=True)

    facebook_profile = models.URLField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = Account.objects.get(id=self.id)
        except Account.DoesNotExist:
            # object is not in db, nothing to worry about
            return
        # is the save due to an update of the actual image file?
        if obj.image and self.image and obj.image != self.image:
            # delete the old image file from the storage in favor of the new
            # file
            obj.image.delete()

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.image.delete()
        return super(Account, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(Account, self).save(*args, **kwargs)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user=instance)
        instance.account.save()

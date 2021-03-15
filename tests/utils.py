from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.generics import GenericAPIView

GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Others", "Others")]


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=6
    )


class ProfileQuerySet(list):
    def count(self, **kwargs):
        return len(self)

    @property
    def model(self):
        return Profile

    def all(self):
        return self


class ViewClass(GenericAPIView):
    def get_queryset(self):
        return ProfileQuerySet()

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    class AgeUnit(models.TextChoices):
        TEEN = 'L1', _('18-19 years old')
        EARLY20 = 'E2', _('20-24 years old')
        LATE20 = 'L2', _('25-29 years old')
        EARLY30 = 'E3', _('30-34 years old')
        LATE30 = 'L3', _('35-39 years old')
        OVER40 = 'O4', _('more than 40 years old')

    class SexType(models.TextChoices):
        MAN = 'M', _('Man')
        WOMAN = 'W', _('Woman')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area = models.CharField(max_length=100)
    age = models.CharField(
        max_length=2,
        choices=AgeUnit.choices,
        default=AgeUnit.TEEN,
    )
    sex = models.CharField(
        max_length=1,
        choices=SexType.choices,
        default=SexType.MAN,
    )

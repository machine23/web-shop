from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_email_unique(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('This email address is already in use.')

from datetime import datetime

from django.db import models


class UserType(models.Model):
    # uuid: str
    username: str
    first_name: str
    last_name: str
    email: str
    is_staff: bool
    is_active: bool
    date_joined: datetime
    email: str
    phone_number: str
    type: str

    class Meta:
        abstract = True

from django.db import models
from .base import TenantAwareModel
from .users import User
import uuid


class Students(TenantAwareModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="students")
    no_of_students = models.IntegerField()
    class Meta:
        db_table = "students"
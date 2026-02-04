from django.db import models
from .model.tenants import Tenant
from .model.users import User
# Create your models here.

__all__ = ["Tenant", "User"]

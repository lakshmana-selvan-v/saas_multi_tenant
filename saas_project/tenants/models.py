from django.db import models
from .model.tenants import Tenant
from .model.users import User
from .model.blogs import Blogs
from .model.favorite import Favorite
from .model.roles import Roles
# Create your models here.

__all__ = ["Tenant", "User", "Blogs", "Favorite", "Roles"]

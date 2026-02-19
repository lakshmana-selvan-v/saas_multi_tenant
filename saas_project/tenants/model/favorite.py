from django.db import models
from .base import TenantAwareModel
from .blogs import Blogs
from .users import User


class Favorite(TenantAwareModel):
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, blank=True, related_name="favorites")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="favorites")

    class Meta:
        db_table = "favorites"
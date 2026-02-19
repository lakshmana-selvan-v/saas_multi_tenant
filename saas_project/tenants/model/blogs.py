from django.db import models
from .base import TenantAwareModel
from .users import User


class Blogs(TenantAwareModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="blogs")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True),
    updated_at = models.DateTimeField(auto_now=True),

    class Meta:
        db_table = "blogs"

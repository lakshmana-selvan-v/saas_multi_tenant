from django.db import models
import uuid


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(db_index=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    
    class Meta:
        db_table = "users"
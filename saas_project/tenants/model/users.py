from django.db import models


class User(models.Model):
    tenant_id = models.IntegerField()
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    
    class Meta:
        db_table = "users"
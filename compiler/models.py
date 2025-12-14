from django.db import models
import uuid
# Create your models here.
class SharedCode(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    language = models.CharField(max_length=20)
    code = models.TextField()
    input_data = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
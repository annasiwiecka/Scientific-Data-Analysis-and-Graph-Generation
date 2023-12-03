from django.db import models
from django.utils import timezone
import uuid

# Create your models here.

class DataModel(models.Model):
    data_name = models.CharField(max_length=100)
    experiment_name = models.CharField(max_length=100, default='')
    measurement_value = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(db_index=True, default=timezone.now)
    processed_data_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return self.data_name
    
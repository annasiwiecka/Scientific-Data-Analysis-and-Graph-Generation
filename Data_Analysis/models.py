from django.db import models
from django.utils import timezone
import uuid

# Create your models here.

class DataName(models.Model):
    name = models.CharField(max_length=100, unique=True)

class TimestampInfo(models.Model):
    data_name = models.ForeignKey(DataName, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(db_index=True, default=timezone.now)

class DataModel(models.Model):
    data_name = models.ForeignKey(DataName, on_delete=models.CASCADE)
    experiment_name = models.CharField(max_length=100, default='')
    measurement_value = models.FloatField(default=0.0)
    timestamp_info = models.ForeignKey(TimestampInfo, on_delete=models.CASCADE)
    processed_data_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return str(self.data_name)
    
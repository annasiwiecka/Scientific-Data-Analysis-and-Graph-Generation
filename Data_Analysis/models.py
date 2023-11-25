from django.db import models

# Create your models here.

class DataModel(models.Model):
    experiment_name = models.CharField(max_length=100)
    measurement_value = models.FloatField()
    timestamp = models.DateTimeField(db_index=True)

    def __str__(self):
        return self.experiment_name
    
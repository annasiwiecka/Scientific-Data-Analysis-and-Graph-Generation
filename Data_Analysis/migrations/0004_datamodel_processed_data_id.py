# Generated by Django 4.2.7 on 2023-12-03 20:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Data_Analysis', '0003_datamodel_data_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='datamodel',
            name='processed_data_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]

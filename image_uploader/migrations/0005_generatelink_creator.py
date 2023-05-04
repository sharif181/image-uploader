# Generated by Django 4.1.7 on 2023-03-01 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image_uploader', '0004_generatelink'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatelink',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

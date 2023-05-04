# Generated by Django 4.1.7 on 2023-02-28 18:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import image_uploader.models


class Migration(migrations.Migration):

    dependencies = [
        ('image_uploader', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('description', models.TextField(blank=True, null=True)),
                ('image_url', models.ImageField(upload_to=image_uploader.models.upload_to)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# Generated by Django 3.1.3 on 2024-04-16 04:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticeboardpost',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

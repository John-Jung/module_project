# Generated by Django 3.1.3 on 2024-04-16 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_noticeboardpost_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticeboardpost',
            name='imgfile',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]

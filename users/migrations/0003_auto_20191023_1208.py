# Generated by Django 2.2.3 on 2019-10-23 12:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_device'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='device',
            options={},
        ),
        migrations.AddField(
            model_name='device',
            name='last_update',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

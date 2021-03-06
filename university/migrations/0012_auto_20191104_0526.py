# Generated by Django 2.2.4 on 2019-11-04 05:26

import django.utils.timezone
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('university', '0011_auto_20191101_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='classtime',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True,
                                                                    default=django.utils.timezone.now,
                                                                    verbose_name='created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classtime',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='classtime',
            name='state',
            field=models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0),
        ),
    ]

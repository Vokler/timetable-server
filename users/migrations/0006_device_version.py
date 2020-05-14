# Generated by Django 2.2.4 on 2019-11-04 20:02

from django.db import migrations, models


def set_api_version(apps, schema):
    Device = apps.get_model('users', 'Device')

    first_api_version = 'v1'
    Device.objects.all().update(version=first_api_version)


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0005_user_last_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='version',
            field=models.CharField(blank=True, help_text='Version of API.', max_length=8, null=True),
        ),
        migrations.RunPython(code=set_api_version),
    ]

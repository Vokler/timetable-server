# Generated by Django 2.1.3 on 2019-04-15 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, unique=True)),
                ('short_title', models.CharField(help_text='Сокращённое название факультета.', max_length=16, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Факультет',
                'verbose_name_plural': 'Факультеты',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('title', models.CharField(max_length=2, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, unique=True)),
                ('short_title', models.CharField(help_text='Сокращённое название направления.', max_length=16, null=True, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('groups', models.ManyToManyField(to='university.Group')),
            ],
            options={
                'verbose_name': 'Направление',
                'verbose_name_plural': 'Направления',
            },
        ),
        migrations.AddField(
            model_name='faculty',
            name='occupations',
            field=models.ManyToManyField(to='university.Occupation'),
        ),
    ]

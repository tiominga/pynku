# Generated by Django 5.2 on 2025-05-01 12:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='database',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='connection',
            name='date_add',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='connection',
            name='host',
            field=models.CharField(default='localhost', max_length=150),
        ),
        migrations.AddField(
            model_name='connection',
            name='name',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='connection',
            name='password',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='connection',
            name='port',
            field=models.IntegerField(default=3306),
        ),
        migrations.AddField(
            model_name='connection',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='connection',
            name='user',
            field=models.CharField(default='root', max_length=150),
        ),
    ]

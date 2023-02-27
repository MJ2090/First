# Generated by Django 4.1.7 on 2023-02-27 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('embedding', '0003_userprofile_left_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenConsumption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('modelType', models.IntegerField(choices=[(0, 'UNKNOWN'), (1, 'EMBEDDING'), (2, 'CHAT'), (3, 'IMAGE'), (4, 'TRANSLATE'), (5, 'GRAMMAR'), (6, 'SUMMARY')], default=0)),
                ('secret', models.CharField(default='', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

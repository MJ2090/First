# Generated by Django 4.1.7 on 2023-03-01 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embedding', '0004_tokenconsumption'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tokenconsumption',
            old_name='modelType',
            new_name='model_type',
        ),
        migrations.RenameField(
            model_name='tokenconsumption',
            old_name='amount',
            new_name='token_amount',
        ),
    ]

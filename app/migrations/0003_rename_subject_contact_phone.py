# Generated by Django 5.1 on 2024-08-27 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='subject',
            new_name='phone',
        ),
    ]

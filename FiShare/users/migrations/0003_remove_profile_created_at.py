# Generated by Django 4.1.5 on 2023-07-02 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='created_at',
        ),
    ]

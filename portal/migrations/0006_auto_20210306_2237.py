# Generated by Django 3.1.7 on 2021-03-06 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_auto_20210306_2237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poll',
            old_name='vites_pass',
            new_name='votes_pass',
        ),
    ]

# Generated by Django 5.0.6 on 2024-07-02 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]

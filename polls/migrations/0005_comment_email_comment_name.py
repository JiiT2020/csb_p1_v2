# Generated by Django 5.0.6 on 2024-07-03 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]

# Generated by Django 4.0.4 on 2022-05-16 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0002_customerdata_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerdata',
            name='OTP',
            field=models.PositiveIntegerField(blank=True, max_length=6, null=True),
        ),
    ]

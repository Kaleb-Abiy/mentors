# Generated by Django 4.2.4 on 2023-09-21 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='hourly_rate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Mentor',
        ),
    ]
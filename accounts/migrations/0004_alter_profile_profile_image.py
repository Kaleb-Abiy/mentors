# Generated by Django 4.2.4 on 2023-09-11 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_mentor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='default.jpg', upload_to='profile_images'),
        ),
    ]
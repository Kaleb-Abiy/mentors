# Generated by Django 4.2.4 on 2023-11-04 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_alter_appointment_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='payment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='appointment', to='feed.payment'),
        ),
    ]
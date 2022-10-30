# Generated by Django 4.1.2 on 2022-10-19 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("device", "0002_alter_device_device_type_alter_device_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="device",
            name="device_type",
            field=models.CharField(
                blank=True,
                choices=[("buoy", "Buoy"), ("mounted", "Mounted")],
                default="buoy",
                help_text="디바이스 타입",
                max_length=50,
            ),
        ),
    ]
# Generated by Django 4.0.4 on 2022-05-27 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buoy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='data',
            options={'ordering': ('-date', '-time')},
        ),
        migrations.RenameField(
            model_name='data',
            old_name='o4e',
            new_name='c4e',
        ),
    ]
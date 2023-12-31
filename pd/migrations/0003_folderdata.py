# Generated by Django 4.2.4 on 2023-10-30 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pd', '0002_remove_filedata_id_filedata_pk_name_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='FolderData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('num_files', models.IntegerField()),
                ('files', models.JSONField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

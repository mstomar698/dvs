# Generated by Django 4.2.1 on 2023-09-29 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bl', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articledetails',
            name='country',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='articledetails',
            name='end_year',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='articledetails',
            name='impact',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='articledetails',
            name='pestle',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='articledetails',
            name='region',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='articledetails',
            name='sector',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='articledetails',
            name='source',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='articledetails',
            name='start_year',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='articledetails',
            name='topic',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

# Generated by Django 3.0.5 on 2020-08-19 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='dataset_name',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.1 on 2020-09-08 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200908_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthapp',
            name='user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]

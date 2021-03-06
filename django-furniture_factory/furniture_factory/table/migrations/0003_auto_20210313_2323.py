# Generated by Django 2.2 on 2021-03-13 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0002_auto_20210313_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='legs',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='table.Leg'),
        ),
        migrations.AlterField(
            model_name='table',
            name='price',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]

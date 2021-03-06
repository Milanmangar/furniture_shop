# Generated by Django 2.2 on 2021-03-13 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feet',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('width', models.IntegerField(blank=True, default=0, null=True)),
                ('length', models.IntegerField(blank=True, default=0, null=True)),
                ('radius', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Leg',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('foldable', models.BooleanField(default=False)),
                ('feet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feet', to='table.Feet')),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('legs', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='table.Leg')),
            ],
        ),
    ]

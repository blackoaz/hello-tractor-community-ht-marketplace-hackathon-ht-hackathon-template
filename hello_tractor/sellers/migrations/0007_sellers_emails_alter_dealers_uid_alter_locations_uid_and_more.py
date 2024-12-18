# Generated by Django 5.1.3 on 2024-11-25 12:16

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0006_alter_dealers_uid_alter_locations_uid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sellers_Emails',
            fields=[
                ('uid', models.UUIDField(default=uuid.UUID('b7724c2d-6871-4e2b-9193-bbe6cf1f1ed6'), editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('customer_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('customer_message', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='dealers',
            name='uid',
            field=models.UUIDField(default=uuid.UUID('b7724c2d-6871-4e2b-9193-bbe6cf1f1ed6'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='locations',
            name='uid',
            field=models.UUIDField(default=uuid.UUID('b7724c2d-6871-4e2b-9193-bbe6cf1f1ed6'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='uid',
            field=models.UUIDField(default=uuid.UUID('b7724c2d-6871-4e2b-9193-bbe6cf1f1ed6'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='tractor',
            name='uid',
            field=models.UUIDField(default=uuid.UUID('b7724c2d-6871-4e2b-9193-bbe6cf1f1ed6'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]

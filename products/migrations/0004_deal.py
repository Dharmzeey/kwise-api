# Generated by Django 5.0.8 on 2024-11-10 19:40

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('details', models.TextField()),
                ('image', models.ImageField(upload_to='deals/%Y/%m')),
                ('link_to', models.URLField()),
            ],
        ),
    ]

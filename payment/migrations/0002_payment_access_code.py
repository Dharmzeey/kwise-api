# Generated by Django 5.0.8 on 2024-10-28 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='access_code',
            field=models.CharField(default='ikw'),
            preserve_default=False,
        ),
    ]

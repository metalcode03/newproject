# Generated by Django 2.2.4 on 2019-09-12 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190911_0513'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='S'),
            preserve_default=False,
        ),
    ]

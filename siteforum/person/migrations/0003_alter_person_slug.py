# Generated by Django 4.2.1 on 2024-07-26 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_alter_person_options_person_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]

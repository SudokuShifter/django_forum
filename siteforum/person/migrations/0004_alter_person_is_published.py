# Generated by Django 4.2.1 on 2024-07-26 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0003_alter_person_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='is_published',
            field=models.BooleanField(choices=[(0, 'Черновик'), (1, 'Опубликовано')], default=0),
        ),
    ]

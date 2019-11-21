# Generated by Django 2.2.7 on 2019-11-13 18:26

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='flats',
            managers=[
                ('flas', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='payments',
            managers=[
                ('paym', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='access',
            name='stype',
            field=models.BooleanField(choices=[(False, 'Осмотр'), (True, 'Аренда')], default=False),
        ),
        migrations.AddField(
            model_name='flats',
            name='app_id',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='flats',
            name='app_status',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='rents',
            name='booking',
            field=models.DateTimeField(null=True, verbose_name='Окончание бронироваия'),
        ),
        migrations.AlterField(
            model_name='flats',
            name='door_status',
            field=models.BooleanField(blank=True, choices=[(False, 'Заблокирована'), (True, 'Доступ открыт')], null=True),
        ),
    ]

# Generated by Django 2.2.3 on 2019-10-02 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0027_usersdocuments_yakey'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersdocuments',
            name='agreement',
            field=models.BooleanField(choices=[(False, 'Не согласен'), (True, 'Согласен')], default=None),
        ),
        migrations.AlterField(
            model_name='usersdocuments',
            name='status',
            field=models.BooleanField(choices=[(False, 'Не согласен'), (True, 'Согласен')], default=False),
        ),
    ]

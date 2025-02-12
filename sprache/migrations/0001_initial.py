# Generated by Django 3.0 on 2020-01-28 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default=None, max_length=80, verbose_name='Электронная почта для отправки чека об оплате')),
                ('first_name', models.CharField(default=None, max_length=80, verbose_name='Имя')),
                ('last_name', models.CharField(default=None, max_length=80, verbose_name='Фамилия')),
                ('price', models.DecimalField(decimal_places=2, default=None, max_digits=10, verbose_name='Сумма')),
                ('key', models.CharField(blank=True, default=None, max_length=80, null=True)),
                ('status', models.BooleanField(default=False, null=True)),
                ('created_at', models.DateTimeField(default=None, null=True)),
                ('payment_id', models.CharField(blank=True, default=None, max_length=50, null=True)),
            ],
        ),
    ]

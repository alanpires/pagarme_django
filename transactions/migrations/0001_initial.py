# Generated by Django 3.2.7 on 2021-09-20 21:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fee', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('description', models.TextField()),
                ('payment_method', models.TextField(choices=[('debit_card', 'debit_card'), ('credit_card', 'credit_card')])),
                ('card_number', models.CharField(max_length=16)),
                ('cardholders_name', models.CharField(max_length=255)),
                ('card_expiring_date', models.DateField(default=django.utils.timezone.now)),
                ('cvv', models.CharField(max_length=255)),
                ('date_transaction', models.DateTimeField(default=django.utils.timezone.now)),
                ('client_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Payable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('paid', 'paid'), ('waiting_funds', 'waiting_funds')], max_length=255, null=True)),
                ('payment_date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('amount_client', models.FloatField(null=True)),
                ('fee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fee.fee')),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='transactions.transaction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 4.0.1 on 2022-01-26 09:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('customer_id', models.IntegerField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_address', models.CharField(max_length=255)),
                ('customer_phonenumber', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
            ],
        ),
        migrations.CreateModel(
            name='employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employee_address', models.CharField(blank=True, max_length=255)),
                ('employee_phonenumber', models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('employee_role', models.CharField(blank=True, choices=[('A', 'Admin'), ('R', 'Receptionist')], max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('product_id', models.IntegerField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('manufacturer_name', models.CharField(max_length=255)),
                ('product_qunatity', models.IntegerField()),
                ('product_expiry', models.DateField()),
                ('product_price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='transction',
            fields=[
                ('transction_id', models.IntegerField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_sum', models.IntegerField()),
                ('customer_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.customer')),
                ('employee_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.employee')),
                ('product_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.product')),
            ],
        ),
    ]

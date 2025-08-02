# Generated manually for initial migration

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsurancePolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_number', models.CharField(editable=False, max_length=10, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('insurance_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.appuser')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.car')),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_type', models.CharField(choices=[('LOYALTY', 'Лоялност'), ('SAFE_DRIVER', 'Без щети'), ('MULTI_POLICY', 'Множествени полици')], max_length=12)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('applicable_to', models.ManyToManyField(blank=True, to='policies.insurancepolicy')),
            ],
        ),
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('PENDING', 'Чакаща'), ('APPROVED', 'Одобрена'), ('REJECTED', 'Отхвърлена')], default='PENDING', max_length=10)),
                ('photos', models.ImageField(blank=True, upload_to='claims/')),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policies.insurancepolicy')),
            ],
        ),
    ] 
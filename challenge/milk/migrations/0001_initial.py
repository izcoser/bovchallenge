# Generated by Django 4.1 on 2022-08-26 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.DecimalField(decimal_places=3, max_digits=8)),
                ('under_50', models.DecimalField(decimal_places=3, max_digits=6)),
                ('over_50', models.DecimalField(decimal_places=3, max_digits=6)),
                ('bonus', models.DecimalField(decimal_places=3, max_digits=6)),
                ('semester', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('distance', models.DecimalField(decimal_places=3, max_digits=8)),
                ('code', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10)),
                ('cnpj', models.CharField(max_length=18)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MilkDeliveries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=3, max_digits=15)),
                ('date', models.DateTimeField()),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='milk.farm')),
            ],
        ),
        migrations.AddField(
            model_name='farm',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='milk.farmer'),
        ),
    ]

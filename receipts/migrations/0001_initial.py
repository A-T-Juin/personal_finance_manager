# Generated by Django 2.1 on 2018-08-06 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('budgets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiptName', models.CharField(max_length=20)),
                ('receiptAmount', models.DecimalField(decimal_places=2, max_digits=11)),
                ('receiptCategory', models.CharField(choices=[('food', 'Food and Drinks'), ('bill', 'Bills'), ('cons', 'Consumer Goods'), ('misc', 'Miscellaneous')], max_length=4)),
                ('receiptDate', models.DateField(blank=True)),
                ('receiptDescription', models.CharField(blank=True, max_length=128)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipts', to='budgets.Budget')),
            ],
        ),
    ]

# Generated by Django 5.2.1 on 2025-06-02 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_target_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='target_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]

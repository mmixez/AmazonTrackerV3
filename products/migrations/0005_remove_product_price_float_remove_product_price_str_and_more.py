# Generated by Django 5.2.1 on 2025-06-01 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price_float',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price_str',
        ),
        migrations.RemoveField(
            model_name='product',
            name='title',
        ),
        migrations.RemoveField(
            model_name='product',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='product',
            name='last_checked',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='last_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='target_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='url',
            field=models.URLField(default='https://example.com/placeholder', unique=True),
            preserve_default=False,
        ),
    ]

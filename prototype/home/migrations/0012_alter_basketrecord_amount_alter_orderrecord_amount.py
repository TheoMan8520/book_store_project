# Generated by Django 4.0.6 on 2023-04-14 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_order_destination_order_post_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketrecord',
            name='amount',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='orderrecord',
            name='amount',
            field=models.IntegerField(),
        ),
    ]

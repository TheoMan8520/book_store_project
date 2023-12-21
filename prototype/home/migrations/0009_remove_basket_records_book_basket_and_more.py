# Generated by Django 4.0.6 on 2023-04-13 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_basket_basketrecord_basket_records_basket_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basket',
            name='records',
        ),
        migrations.AddField(
            model_name='book',
            name='basket',
            field=models.ManyToManyField(related_name='inbasket_books', through='home.BasketRecord', to='home.basket'),
        ),
        migrations.AlterField(
            model_name='basketrecord',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.book'),
        ),
    ]

# Generated by Django 4.0.6 on 2023-04-11 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='content_type',
            field=models.CharField(help_text='The MIMEType of the file', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='picture',
            field=models.BinaryField(editable=True, null=True),
        ),
    ]
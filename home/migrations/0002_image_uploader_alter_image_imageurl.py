# Generated by Django 4.0.4 on 2022-04-26 04:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='uploader',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='imageURL',
            field=models.TextField(default='', max_length=200),
        ),
    ]

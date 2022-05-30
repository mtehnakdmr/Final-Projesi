# Generated by Django 4.0.4 on 2022-04-26 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_image_uploader_alter_image_imageurl'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='images')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('uploader', models.CharField(max_length=20)),
                ('imageURL', models.TextField(default='', max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]

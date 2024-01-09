# Generated by Django 3.1.1 on 2023-12-22 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='file_upload',
            field=models.FileField(blank=True, upload_to='blog/files/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='post',
            name='head_image',
            field=models.ImageField(blank=True, upload_to='blog/images/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='post',
            name='hook_text',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

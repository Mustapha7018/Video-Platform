# Generated by Django 5.0.6 on 2024-06-18 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veedeo', '0003_alter_video_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(default='thumbnails/camera.jpg', upload_to='thumbnails/'),
        ),
    ]
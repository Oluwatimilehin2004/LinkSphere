# Generated by Django 5.1.5 on 2025-01-29 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='banner',
            field=models.ImageField(blank=True, default='banner/backdrop-blur.png', upload_to='banner'),
        ),
    ]

# Generated by Django 3.2 on 2021-04-28 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MobileProvidersApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='profilePicture',
            field=models.ImageField(blank=True, null=True, upload_to='profilePicture'),
        ),
    ]

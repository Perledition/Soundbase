# Generated by Django 2.0.6 on 2018-10-05 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElectronicData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Artist', models.CharField(max_length=100)),
                ('song_title', models.CharField(max_length=50)),
                ('link', models.CharField(max_length=200)),
            ],
        ),
    ]

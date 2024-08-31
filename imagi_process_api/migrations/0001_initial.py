# Generated by Django 5.1 on 2024-08-30 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('input_urls', models.TextField()),
                ('output_urls', models.TextField(blank=True, null=True)),
            ],
        ),
    ]

# Generated by Django 4.1.1 on 2022-11-05 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rtitle', models.CharField(max_length=30, null=True)),
                ('rexplain', models.CharField(max_length=300, null=True)),
                ('user', models.CharField(max_length=10, null=True)),
                ('rimage', models.ImageField(upload_to=None)),
            ],
        ),
    ]
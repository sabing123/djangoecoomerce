# Generated by Django 3.1.3 on 2021-01-30 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20201204_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contact_id', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=50)),
                ('email', models.CharField(default='', max_length=50)),
                ('pnumber', models.CharField(default='', max_length=30)),
                ('country', models.CharField(default='', max_length=300)),
                ('subject', models.CharField(default='', max_length=500)),
            ],
        ),
    ]

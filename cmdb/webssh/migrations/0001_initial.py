# Generated by Django 3.2 on 2023-12-28 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='id')),
                ('hostname', models.CharField(max_length=32, verbose_name='主机名')),
                ('ipaddr', models.CharField(max_length=32, verbose_name='IP地址')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'unique_together': {('hostname', 'ipaddr')},
            },
        ),
    ]

# Generated by Django 3.2 on 2024-01-03 03:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JkBase',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='id')),
                ('jenkinsname', models.CharField(max_length=255, verbose_name='jenkins名字')),
                ('jenkinsurl', models.CharField(max_length=255, verbose_name='jenkins地址')),
                ('username', models.CharField(max_length=255, verbose_name='jenkins账号')),
                ('password', models.CharField(max_length=255, verbose_name='jenkins密码')),
                ('token', models.CharField(max_length=255, verbose_name='jenkins的token')),
            ],
        ),
        migrations.CreateModel(
            name='Jkjob',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='id')),
                ('jobname', models.CharField(max_length=255, verbose_name='jenkins名字')),
                ('joburl', models.CharField(max_length=255, verbose_name='jenkins地址')),
                ('JkId', models.ManyToManyField(to='jenkinsJob.JkBase')),
            ],
        ),
        migrations.CreateModel(
            name='JkbuildJob',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='id')),
                ('buildlog', models.CharField(max_length=255, verbose_name='发版日志')),
                ('submitter', models.CharField(max_length=255, verbose_name='提交人')),
                ('publisher', models.CharField(max_length=255, verbose_name='发版人')),
                ('buildtime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发版时间')),
                ('jobId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='jenkinsJob.jkjob')),
            ],
        ),
    ]

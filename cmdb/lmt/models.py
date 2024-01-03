from django.db import models


# Create your models here.
class lmt(models.Model):
    id = models.CharField(verbose_name='id',max_length=32, primary_key=True)
    username = models.CharField(verbose_name='账号', max_length=255)
    password = models.CharField(verbose_name='密码', max_length=255)
    webport = models.IntegerField(verbose_name='web端口',blank=True,null=True)
    appID = models.IntegerField(verbose_name='appid',blank=True,null=True)
    appSecret = models.CharField(verbose_name='APPSecret',blank=True, null=True,max_length=255)
    sxtZS = models.IntegerField(verbose_name='摄像头总数',blank=True,null=True)
    sxtQYS = models.IntegerField(verbose_name='摄像头启用数',blank=True,null=True)
    sxtZXS = models.IntegerField(verbose_name='摄像头在线数',blank=True,null=True)
    description = models.TextField(verbose_name='描述',blank=True,null=True)

    class Meta:
        db_table = 'lmt'
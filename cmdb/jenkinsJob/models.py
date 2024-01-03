from django.db import models
import django.utils.timezone as timezone
from rest_framework.decorators import api_view


# Create your models here.
class JkBase(models.Model):
    id = models.AutoField(verbose_name='id', primary_key=True)
    jenkinsname = models.CharField(verbose_name='jenkins名字', max_length=255)
    jenkinsurl = models.CharField(verbose_name='jenkins地址', max_length=255)
    username = models.CharField(verbose_name='jenkins账号', max_length=255)
    password = models.CharField(verbose_name='jenkins密码', max_length=255)
    token = models.CharField(verbose_name='jenkins的token', max_length=255)
    # 与AuthorDetail建立一对一的关系，一对一的这个关系字段写在两个表的任意一个表里面都可以
    # authorDetail = models.OneToOneField(to="AuthorDetail", to_field="id",
    #                                     on_delete=models.CASCADE)  # 就是foreignkey+unique，只不过不需要我们自己来写参数了，并且orm会自动帮你给这个字段名字拼上一个_id，数据库中字段名称为authorDetail_id

    def __str__(self):
        return self.name

class Jkjob(models.Model):
    id = models.AutoField(verbose_name='id', primary_key=True)
    jobname = models.CharField(verbose_name='jenkins名字', max_length=50)
    joburl = models.CharField(verbose_name='jenkins地址', max_length=255)

    # 与Publish建立一对多的关系,外键字段建立在多的一方，字段publish如果是外键字段，那么它自动是int类型
    # jenkinsJob = models.ForeignKey(to="Jenkins", to_field="id", on_delete=models.CASCADE)
    # foreignkey里面可以加很多的参数，都是需要咱们学习的，慢慢来，to指向表，to_field指向你关联的字段，不写这个，默认会自动关联主键字段，on_delete级联删除字段名称不需要写成publish_id，orm在翻译foreignkey的时候会自动给你这个字段拼上一个_id,这个字段名称在数据库里面就自动变成了publish_id
    # 与Author表建立多对多的关系,ManyToManyField可以建在两个模型中的任意一个，自动创建第三张表，并且注意一点，你查看book表的时候，你看不到这个字段，因为这个字段就是创建第三张表的意思，不是创建字段的意思，所以只能说这个book类里面有authors这个字段属性
    JkId = models.ManyToManyField(to='JkBase', )  # 注意不管是一对多还是多对多，写to这个参数的时候，最后后面的值是个字符串，不然你就需要将你要关联的那个表放到这个表的上面


    def __str__(self):
        return self.name

class JkbuildJob(models.Model):
    id = models.AutoField(verbose_name='id', primary_key=True)
    buildlog = models.CharField(verbose_name='发版日志', max_length=255)
    submitter = models.CharField(verbose_name='提交人', max_length=255)
    publisher = models.CharField(verbose_name='发版人', max_length=255)
    buildtime = models.DateTimeField(verbose_name='发版时间', default = timezone.now)
    jobId = models.OneToOneField(to="Jkjob", to_field="id",
                         on_delete=models.CASCADE)
    # 与Publish建立一对多的关系,外键字段建立在多的一方，字段publish如果是外键字段，那么它自动是int类型
    # jenkinsJob = models.ForeignKey(to="Jenkins", to_field="id", on_delete=models.CASCADE)
    # foreignkey里面可以加很多的参数，都是需要咱们学习的，慢慢来，to指向表，to_field指向你关联的字段，不写这个，默认会自动关联主键字段，on_delete级联删除字段名称不需要写成publish_id，orm在翻译foreignkey的时候会自动给你这个字段拼上一个_id,这个字段名称在数据库里面就自动变成了publish_id
    # 与Author表建立多对多的关系,ManyToManyField可以建在两个模型中的任意一个，自动创建第三张表，并且注意一点，你查看book表的时候，你看不到这个字段，因为这个字段就是创建第三张表的意思，不是创建字段的意思，所以只能说这个book类里面有authors这个字段属性
    # joburl = models.ManyToManyField(to='Jenkins', )  # 注意不管是一对多还是多对多，写to这个参数的时候，最后后面的值是个字符串，不然你就需要将你要关联的那个表放到这个表的上面

    def __str__(self):
        return self.name


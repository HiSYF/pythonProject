from rest_framework.serializers import ModelSerializer

from .models import *

class JenkinsSerializer(ModelSerializer):
    """序列化与反序列化数据时可以使用"""

    class Meta:
        model = JkBase
        fields = '__all__'

class EditJenkinsSerializer(ModelSerializer):
    """编辑数据反序列化器"""
    class Meta:
        model = JkBase
        exclude = ('attachments',)  # 若编辑文件接口提交时文件为空，此时不需要序列化此字段

class TeamJenkinsQuerySerializer(ModelSerializer):
    """查询所有数据的序列化器"""
    # attachments = TeamDataStructureFileField(queryset=TeamDataStructureFile.objects.all(), many=True)
    class Meta:
        model = JkBase
        fields = '__all__'


class jobSerializer(ModelSerializer):
    """序列化与反序列化数据时可以使用"""

    class Meta:
        model = Jkjob
        fields = '__all__'

class EditjobSerializer(ModelSerializer):
    """编辑数据反序列化器"""
    class Meta:
        model = Jkjob
        exclude = ('attachments',)  # 若编辑文件接口提交时文件为空，此时不需要序列化此字段

class TeamjobQuerySerializer(ModelSerializer):
    """查询所有数据的序列化器"""
    # jenkinsJob = JenkinsSerializer(queryset=Jenkins.objects.all(), many=True)
    class Meta:
        model = Jkjob
        fields = '__all__'




class buildJobSerializer(ModelSerializer):
    """序列化与反序列化数据时可以使用"""

    class Meta:
        model = JkbuildJob
        fields = '__all__'

class EditbuildJobSerializer(ModelSerializer):
    """编辑数据反序列化器"""
    class Meta:
        model = JkbuildJob
        exclude = ('attachments',)  # 若编辑文件接口提交时文件为空，此时不需要序列化此字段

class TeambuildJobQuerySerializer(ModelSerializer):
    """查询所有数据的序列化器"""
    # job = jobSerializer(queryset=job.objects.all(), many=True)
    class Meta:
        model = JkbuildJob
        fields = '__all__'
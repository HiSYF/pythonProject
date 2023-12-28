from rest_framework import serializers
from .models import Host
class HostModelSerializers(serializers.Serializer):
    id = serializers.CharField()
    hostname = serializers.CharField()
    ipaddr = serializers.CharField()
    create_time = serializers.DateTimeField()

    # 在对应的序列化模型类下实现create()方法
    def create(self, validated_data):
        """
        :param validated_data: 校验之后的数据
        **validated_data:把字典进行拆包
        :return:
        """
        # 新增一本图书
        data = Host.objects.create(**validated_data)
        return data

    # 在对应的序列化模型类下实现update()方法
    # 具体实现方法可以不尽相同，这里只是提供一种思路，仅供参考
    def update(self, instance, validated_data):
        """
        :param instance: 创建序列化器时，传入的实例对象
        :param validated_data: 校验之后的数据
        """
        instance.id = validated_data.get('id')
        instance.hostname = validated_data.get('hostname')
        instance.ipaddr = validated_data.get('ipaddr')

        # 更新instance
        instance.save()

        # 返回instance
        return instance

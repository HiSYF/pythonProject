from rest_framework import serializers
from .models import lmt
class LmtModelSerializers(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    webport = serializers.IntegerField(allow_null=True)
    appID = serializers.IntegerField(allow_null=True)
    appSecret = serializers.CharField(allow_null=True,allow_blank=True)
    sxtZS = serializers.IntegerField(allow_null=True)
    sxtQYS = serializers.IntegerField(allow_null=True)
    sxtZXS = serializers.IntegerField(allow_null=True)
    description = serializers.CharField(allow_null=True)

    # 在对应的序列化模型类下实现create()方法
    def create(self, validated_data):
        """
        :param validated_data: 校验之后的数据
        **validated_data:把字典进行拆包
        :return:
        """
        # 新增一本图书
        data = lmt.objects.create(**validated_data)
        return data

    # 在对应的序列化模型类下实现update()方法
    # 具体实现方法可以不尽相同，这里只是提供一种思路，仅供参考
    def update(self, instance, validated_data):
        """
        :param instance: 创建序列化器时，传入的实例对象
        :param validated_data: 校验之后的数据
        """
        instance.username = validated_data.get('username')
        instance.password = validated_data.get('password')
        instance.webport = validated_data.get('webport')
        instance.appSecret = validated_data.get('appSecret')
        instance.appID = validated_data.get('appID')
        instance.sxtZS = validated_data.get('sxtZS')
        instance.sxtQYS = validated_data.get('sxtQYS')
        instance.sxtZXS = validated_data.get('sxtZXS')

        # 更新instance
        instance.save()

        # 返回instance
        return instance

from rest_framework import serializers


class DrainPipeSerializer(serializers.Serializer):
    IDN = serializers.CharField(max_length=15)
    GUBN = serializers.CharField(max_length=15)
    GUBN_NAM = serializers.CharField(max_length=15)
    MEA_YMD = serializers.CharField(max_length=30)
    MEA_WAL = serializers.CharField(max_length=15)
    SIG_STA = serializers.CharField(max_length=15)
    REMARK = serializers.CharField(max_length=100)


class RainFallSerializer(serializers.Serializer):
    RAINGAUGE_CODE = serializers.CharField(max_length=15)
    RAINGAUGE_NAME = serializers.CharField(max_length=15)
    GU_CODE = serializers.CharField(max_length=15)
    GU_NAME = serializers.CharField(max_length=15)
    RAINFALL10 = serializers.CharField(max_length=15)
    RECEIVE_TIME = serializers.CharField(max_length=30)

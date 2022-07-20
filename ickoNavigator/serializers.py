from rest_framework import serializers
from .models import *


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ["target_id", "name", "code", "phone", "type_enum_id_id"]


class GPSSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSData
        fields = ["timestamp", 'latitude', 'longitude', 'speed', 'targetID', 'N_S', 'W_E']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusData
        fields = ["timestamp", 'loadSkew', 'loadPresent', 'latchHealth',
                  'loadHealth', 'positionVerify', 'spoofPresent',
                  'gpsVerify', 'incomingCall', 'outgoingCall', 'targetID',]


class CallLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = [
            "fromWhom",
            "toWhom",
            "timestampStart",
            "callLength",
        ]


class CallQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = CallQuery
        fields = [
            "toWhom",
            "timeQueryMade",
            "CallMade",
        ]


class LoadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loading
        fields = [
            "responsibleMachineID",
            "loadedTimestamp",
            "unloadedTimestamp",
            "fromSite",
            "fromLatitude",
            "fromLongitude",
            "toSite",
            "toLatitude",
            "toLongitude",
            "underLoadDuration",
            "pavedDistance",
        ]


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = [
            "name",
            "latitude",
            "longitude",
            "description",
            "enum_id",
        ]

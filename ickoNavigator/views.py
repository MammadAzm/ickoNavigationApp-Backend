from django.http import HttpResponseRedirect

from .Constants import *
from .distanceMeasurement import distanceMeasure

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import *

import json
import datetime
from ickoNavigator.models import *

from django.contrib.auth import authenticate


# Draft Views
# CallLogApiView for when the module sends the call log.
class CallLogApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response("Get Not Supported", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        data = request.body
        data = data.decode('UTF-8')
        data = data.split(",")
        fromWhom = int(data[0])
        toWhom = int(data[1])
        timestampStart = float(data[2])
        callLength = int(data[3])  # in seconds
        CallLog.objects.create(
            fromWhom=Target.objects.get(target_id=fromWhom),
            toWhom=Target.objects.get(target_id=toWhom),
            timestampStart=timestampStart,
            callLength=callLength,
        ).save()
        return Response(data="Call Logged", status=status.HTTP_200_OK)


# Create your views here.
class GetAssetsApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        data = []
        machines = Target.objects.all()
        for item in machines:
            data.append(item)
        serializer = TargetSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        pass


class GPSDataApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        data = []
        for target in Target.objects.all():
            # print(list(GPSData.objects.filter(targetID=target.target_id)))
            objs = list(GPSData.objects.filter(targetID=target.target_id))
            data.append(objs[-1]) if len(objs) > 0 else None

        serializer = GPSSerializer(data, many=True)
        # print("===================================")
        # print("===================================")
        # print("===================================")
        # print(serializer)
        # print(serializer.data)
        # serializer.data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.body
        data = data.decode('UTF-8')
        if "$" not in data:
            resp = "Failed"
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)
        else:
            index = data.index("$")
            data = data[index:].split(",")
            # data = data.split(",")
            print("=====================")
            print(data)
            print("=====================")
            targetID = int(data[-1][4:])
            print(targetID)
            # targetID = 1
            if data[2] == "A":
                obj = {
                    "timestamp": datetime.datetime.now().timestamp(),
                    "latitude": data[3],
                    "longitude": data[5],
                    "speed": float(data[7]),
                    "targetID": Target.objects.get(target_id=targetID).target_id,
                    "N_S": Enumeration.objects.get(enum_id=data[4]).id,
                    "W_E": Enumeration.objects.get(enum_id=data[6]).id,
                }
                serializer = GPSSerializer(data=obj)
                if serializer.is_valid():
                    serializer.save()
                    resp = "Valid"
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    resp = "Invalid"
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response("Get Not Supported", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        data = request.body
        data = data.decode('UTF-8')

        D0, D1, D2, D3, D4 = data[0], data[1], data[2], data[3], data[4],
        D5, D6, D7, D8, D9 = data[5], data[6], data[7], data[8], data[9],

        obj = {
            "timestamp": datetime.datetime.now().timestamp(),
            "loadSkew": True if int(D0) == 1 else False,
            "loadPresent": True if int(D1) == 1 else False,
            "latchHealth": True if int(D2) == 1 else False,
            "loadHealth": True if int(D3) == 1 else False,
            "positionVerify": True if int(D4) == 1 else False,
            "spoofPresent": True if int(D5) == 1 else False,
            "gpsVerify": True if int(D6) == 1 else False,
            "incomingCall": True if int(D7) == 1 else False,
            "outgoingCall": True if int(D8) == 1 else False,
            "targetID": Target.objects.get(target_id=int(D9)).target_id,
        }

        serializer = StatusSerializer(data=obj)

        previous_obj = list(StatusData.objects.filter(targetID_id=D9))[-1]
        currentLoc = list(GPSData.objects.filter(targetID_id=D9))[-1]
        currentSite = None
        if previous_obj.loadPresent is False and obj['loadPresent'] is True:
            # TODO : Site Estimation Logic::> -- Begins ===================================
            sites = Site.objects.all()
            for site in sites:
                distance = distanceMeasure(site.latitude, site.longitude, currentLoc.latitude, currentLoc.longitude)
                if distance <= gpsAccuracy:
                    currentSite = site
                    break
                else:
                    pass
            # TODO : Site Estimation Logic::> -- Ends =====================================
            if currentSite is None:
                return Response(SITE_NOT_ESTIMATED_MESSAGE, status=status.HTTP_400_BAD_REQUEST)
            Loading.objects.create(
                responsibleMachine=Target.objects.get(target_id=D9),
                loadedTimestamp=datetime.datetime.now().timestamp(),
                unloadedTimestamp=None,
                fromSite=currentSite,
                fromLatitude=currentLoc.latitude,
                fromLongitude=currentLoc.longitude,
                toSite=None,
                toLatitude=None,
                toLongitude=None,
                underLoadDuration=None,
            ).save()
        elif previous_obj.loadPresent is True and obj['loadPresent'] is False:
            # TODO : Site Estimation Logic::> -- Begins ===================================
            sites = Site.objects.all()
            for site in sites:
                distance = distanceMeasure(site.latitude, site.longitude, currentLoc.latitude, currentLoc.longitude)
                if distance <= gpsAccuracy:
                    currentSite = site
                    break
                else:
                    pass
            # TODO : Site Estimation Logic::> -- Ends =====================================
            if currentSite is None:
                return Response(SITE_NOT_ESTIMATED_MESSAGE, status=status.HTTP_400_BAD_REQUEST)
            load = list(Loading.objects.filter(responsibleMachine=D9))[-1]
            pavedDistance = distanceMeasure(currentLoc.latitude, currentLoc.longitude, load.fromLatitude, load.fromLongitude)
            load.unloadedTimestamp = datetime.datetime.now().timestamp()
            load.toLatitude = currentLoc.latitude
            load.toLongitude = currentLoc.longitude
            load.toSite(currentSite)
            load.pavedDistance(pavedDistance)
            load.underLoadDuration = (datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()) - datetime.datetime.fromtimestamp(load.loadedTimestamp)).total_seconds()
            load.save()

        if previous_obj.incomingCall is False and obj['incomingCall'] is True:
            CallLog.objects.create(
                fromWhom=Target.objects.get(type_enum_id=Enumeration.objects.get(enum_id="ControlRoom").id),
                toWhom=Target.objects.get(target_id=D9),
                timestampStart=datetime.datetime.now().timestamp(),
                timestampEnd=None,
                callLength=None,
            ).save()
        elif previous_obj.incomingCall is True and obj['incomingCall'] is False:
            log = list(CallLog.objects.filter(toWhom_id=D9))[-1]
            time = datetime.datetime.now().timestamp()
            log.timestampEnd = time
            log.callLength = (datetime.datetime.fromtimestamp(time) - datetime.datetime.fromtimestamp(log.timestampStart)).total_seconds()
            log.save()

        elif previous_obj.outgoingCall is False and obj['outgoingCall'] is True:
            CallLog.objects.create(
                fromWhom=Target.objects.get(target_id=D9),
                toWhom=Target.objects.get(type_enum_id=Enumeration.objects.get(enum_id="ControlRoom").id),
                timestampStart=datetime.datetime.now().timestamp(),
                timestampEnd=None,
                callLength=None,
            ).save()
        elif previous_obj.outgoingCall is True and obj['outgoingCall'] is False:
            log = list(CallLog.objects.filter(fromWhom_id=D9))[-1]
            time = datetime.datetime.now().timestamp()
            log.timestampEnd = time
            log.callLength = (datetime.datetime.fromtimestamp(time) - datetime.datetime.fromtimestamp(
                log.timestampStart)).total_seconds()
            log.save()

        if serializer.is_valid():
            serializer.save()
            resp = "Valid"
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            resp = "Invalid"
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPhoneApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            call = CallQuery.objects.get(CallMade=False)
            phone = call.phone
            call.CallMade = True
            call.save()
            phone = {
                'phone': str(phone),
            }
            phone = json.dumps(phone)
            return Response(phone, status=status.HTTP_200_OK)
        except CallQuery.DoesNotExist:
            return Response(-1, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        return Response(data="Post Not Supported", status=status.HTTP_400_BAD_REQUEST)


class PassPhone_and_MakeCallQuery(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get(self, request, moduleID, *args, **kwargs):
        try:
            phone = Target.objects.get(target_id=moduleID).phone
            try:
                callExists = CallQuery.objects.get(CallMade=False)
                callExists.delete()
            except CallQuery.DoesNotExist:
                pass
            CallQuery.objects.create(
                toWhom=Target.objects.get(target_id=moduleID),
                timeQueryMade=datetime.datetime.now().timestamp(),
                phone=phone,
                CallMade=False,
            ).save()
            return Response(1, status=status.HTTP_200_OK)
        except Exception:
            return Response(-1, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        return Response("Post Not Supported", status=status.HTTP_400_BAD_REQUEST)


class RawHistoryAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get(self, request, moduleID, startTimeStamp, tillTimeStamp,  *args, **kwargs):
        try:
            target = Target.objects.get(target_id=moduleID)
            startTimeStamp = float(startTimeStamp)
            tillTimeStamp = float(tillTimeStamp)

            loadingRecords = Loading.objects.filter(responsibleMachineID=target.target_id)
            data = []
            for record in loadingRecords:
                if record.unloadedTimestamp:
                    if record.loadedTimestamp >= startTimeStamp and record.unloadedTimestamp <= tillTimeStamp:
                        data.append(record)

            serializer = LoadingSerializer(data=data, many=True)
            serializer.is_valid()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Target.DoesNotExist:
            return Response("Invalid Machine ID", status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response("Invalid Given Timestamps", status=status.HTTP_400_BAD_REQUEST)


def rawHistory_redirect(request, moduleID):
    tillTimeStamp = int(datetime.datetime.now().timestamp())
    startTimeStamp = tillTimeStamp - datetime.timedelta(days=30).total_seconds()
    return HttpResponseRedirect(f'{startTimeStamp}to{tillTimeStamp}')


class ActivityHistoryAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        data = request.POST
        # targetID = data['machID']
        intervalLen = INTERVALS[data['intervalType']]
        intervalsCount = int(data['count'])
        startTimestamp = (datetime.datetime.now().timestamp()) - (intervalLen * intervalsCount)
        if data['machID'] == ALL_TARGETS:
            targets = Target.objects.all()
        else:
            targets = Target.objects.filter(target_id=data['machID'])
        activity = {}
        for target in targets:
            intervals = {}
            loadings = Loading.objects.filter(responsibleMachineID=target.target_id)
            for index in range(1, intervalsCount+1):
                duration = 0
                for loading in loadings:
                    if loading.loadedTimestamp >= startTimestamp+((index-1)*intervalLen) and \
                            loading.unloadedTimestamp <= startTimestamp+(index*intervalLen):
                        duration += loading.underLoadDuration
                intervals[f'interval{intervalsCount+1-index}'] = duration
            activity[target.target_id] = intervals

        return Response(activity, status=status.HTTP_200_OK)


class LoadHistoryAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        data = request.POST
        intervalLen = INTERVALS[data['intervalType']]
        intervalsCount = int(data['count'])
        startTimestamp = (datetime.datetime.now().timestamp()) - (intervalLen * intervalsCount)
        if data['machID'] == ALL_TARGETS:
            targets = Target.objects.all()
        else:
            targets = Target.objects.filter(target_id=data['machID'])
        loadHist = {}
        for target in targets:
            intervals = {}
            loadings = Loading.objects.filter(responsibleMachineID=target.target_id)
            for index in range(1, intervalsCount+1):
                count = 0
                for loading in loadings:
                    if loading.loadedTimestamp >= startTimestamp+((index-1)*intervalLen) and \
                                loading.unloadedTimestamp <= startTimestamp+(index*intervalLen):
                        count += 1
                intervals[f'interval{intervalsCount+1-index}'] = count
            loadHist[target.target_id] = intervals

        return Response(loadHist, status=status.HTTP_200_OK)




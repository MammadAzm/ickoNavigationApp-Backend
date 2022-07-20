import random

import self as self
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncConsumer
import threading
import json
import time

import asyncio

from ickoNavigator.models import *
from ickoNavigator.serializers import *
from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async

from django.contrib.auth import authenticate


class UpdateData(AsyncWebsocketConsumer):
    async def connect(self):
        print("=======================================")
        print("=======================================")
        print("Something has Connected... !!!!!")
        print("=======================================")
        print("=======================================")
        self.groupname = 'dashboard'
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )

        # print(self.scope)
        # print("=============================")
        # print(self.scope['user'])
        # print("=================================")
        # print(self.scope['headers'][-1])
        # print("=================================")
        # print((self.scope['headers'][-1][0]).decode('UTF-8'))
        # print((self.scope['headers'][-1][1]).decode('UTF-8'))
        # print("=================================")
        # print((self.scope['headers'][-2][0]).decode('UTF-8'))
        # print((self.scope['headers'][-2][1]).decode('UTF-8'))

        self.uname = (self.scope['headers'][-2][1]).decode('UTF-8')
        self.passw = (self.scope['headers'][-1][1]).decode('UTF-8')
        self.user = await self.auth(self.uname, self.passw)
        if self.user:
            await self.accept()
            # dataStatus = []
            # dataGPS = []
            data = {}
            targets = await self.getAllTargets()
            for target in targets:
                objGPS = await self.getGPS_for_targetID(target.target_id)
                objStatus = await self.getStatus_for_targetID(target.target_id)
                # print("Here")
                dataGPS = GPSSerializer(objGPS[-1]).data if len(objGPS) > 0 else None
                dataStatus = StatusSerializer(objStatus[-1]).data if len(objStatus) > 0 else None

                data[target.target_id] = {
                    'gps': dataGPS,
                    'status': dataStatus,
                }
            data = json.dumps(data)

            # dataGPS = [GPSSerializer(item).data for item in dataGPS]
            # dataGPS = {'data': dataGPS}

            # dataStatus = [StatusSerializer(item).data for item in dataStatus]
            # dataStatus = {'data': dataStatus}
            # data = {
            #     'gps': dataGPS,
            #     'status': dataStatus,
            # }

            await self.send(text_data=data)

        else:
            # await self.send("Wrong Username or Password")
            await self.close()

    async def disconnect(self, close_code):
        print("=======================================")
        print("Something has Disconnected... !!!!!")
        print("=======================================")
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        print(">>>>>", text_data)
        if text_data == "repeat":
            dataStatus = []
            dataGPS = []
            targets = await self.getAllTargets()
            for target in targets:
                objGPS = await self.getGPS_for_targetID(target.target_id)
                objStatus = await self.getStatus_for_targetID(target.target_id)
                # print("Here")
                dataGPS.append(objGPS[-1]) if len(objGPS) > 0 else None
                dataStatus.append(objStatus[-1]) if len(objStatus) > 0 else None
                # print('There')
            # print(data)
            dataGPS = [GPSSerializer(item).data for item in dataGPS]
            dataGPS = {'data': dataGPS}

            dataStatus = [StatusSerializer(item).data for item in dataStatus]
            dataStatus = {'data': dataStatus}
            data = {
                'gps': dataGPS,
                'status': dataStatus,
            }

            await self.send(text_data=json.dumps(data))

        else:
            print("No Rebound... :)")
        """
        # await self.channel_layer.group_send(
        #     self.groupname,
        #     {
        #         'type': 'deprocessing',
        #         'value': text_data,
        #     }
        # )
    # async def deprocessing(self, event):
    #     value = event['value']
    #     # await self.send(text_data=json.dumps({'value': value}))
    #     await self.send(text_data=json.dumps({'value': value}))
        """

    @sync_to_async
    def getGPS_for_targetID(self, targetID):
        # obj = list(GPSData.objects.filter(targetID=targetID))
        # print("********************")
        # print(obj)
        # print("********************")
        return list(GPSData.objects.filter(targetID=targetID)) #obj

    @sync_to_async
    def getStatus_for_targetID(self, targetID):
        return list(StatusData.objects.filter(targetID=targetID))

    @sync_to_async
    def getAllTargets(self, ):
        return list(Target.objects.all())


    @sync_to_async
    def auth(self, uname, passw):
        return authenticate(username=uname, password=passw)























class Consumer21(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

        data = []
        targets = await self.getAllTargets()
        for target in targets:
            objs = await self.getGPS_for_targetID(target.target_id)
            print("Here")
            data.append(objs[-1]) if len(objs) > 0 else None
            print('There')
        print(data)
        data = [GPSSerializer(item).data for item in data]
        data = {'data': data}
        # data = {
        #     'data' : data
        # }
        # data = json.dumps(data)

        # serializer = GPSSerializer(data, many=True)
        # print("||||||||||||||||||||||||||||||||||||||")
        # print(serializer)
        # print("||||||||||||||||||||||||||||||||||||||")
        # print(serializer.data)
        # print("||||||||||||||||||||||||||||||||||||||")
        # print(str(serializer.data))
        # s = json.dumps(serializer)
        # print(s)
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(data),
        })

        # while self.connected:
        #     await asyncio.sleep(2)
        #     print("here")
        #     obj = "HELLO WORLD" # do_something (Ex: constantly query DB...)
        #     # await self.websocket_receive("Hello To You")
        #     await self.send({
        #         'type': 'websocket.send',
        #         'text':   obj,
        #     })


    async def websocket_receive(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        print("disconnected", event)


    @sync_to_async
    def getGPS_for_targetID(self, targetID):
        obj = list(GPSData.objects.filter(targetID=targetID))
        print("********************")
        print(obj)
        print("********************")
        return obj


    @sync_to_async
    def getAllTargets(self,):
        return list(Target.objects.all())
import os
import configparser
import requests
import json


class Canary:
    baseUrl = "https://my.canary.is/api/"

    def __init__(self, configFile):
        self.accessToken = None
        self.devices = None
        self.customers = None
        self.home_id = None
        self.config = configparser.ConfigParser()
        self.configFileName = configFile
        self.loadConfigFile(self.configFileName)
        self.xsrf_token = None
        self.session= None

    def loadConfigFile(self, configFileName):
        #print('read config file')
        if not(os.path.isfile(configFileName)):
            exit(1)
        self.config.read(configFileName)

    def getAccessToken(self):
        payload = {}
        payload["username"] = self.config["security"]["username"]
        payload["password"] = self.config["security"]["password"]

        try:
            # get necessary header information
            headers = {'Accept-Encoding': 'identity'}
            response=requests.get("https://my.canary.is/login", headers=headers)
            response.raise_for_status()
            #a_resp=json.loads(response.headers)
            s=response.headers["set-cookie"].split(';')
            for astring in s:
                if "XSRF-TOKEN" in astring:
                    self.xsrf_token=astring.split('=')[1]
                if "ssesyranac" in astring:
                    self.session=astring.split('=')[1]
            #print(self.xsrf_token)
            #print(self.session)
            
            # with header information available log in
            if len(self.session)>10:
                headers={}
                headers["X-XSRF-TOKEN"]=self.xsrf_token
                headers["Cookie"]= "ssesyranac=" + self.session
                response = requests.post("https://my.canary.is/api/auth/login", data=payload, headers=headers)
                response.raise_for_status()
                s=response.headers["set-cookie"].split(';')
                for astring in s:
                    if "XSRF-TOKEN" in astring:
                        self.xsrf_token=astring.split('=')[1]
                        #print("xsrf_token updated")
                    if "ssesyranac" in astring:
                        self.session=astring.split('=')[1]
                access_token = response.json()["access_token"]
                self.accessToken = access_token
                #print(access_token)
            return "OK"

        except requests.exceptions.HTTPError as error:
            # print('Request Exception:')
            # print(response.request.body )
            # print(response.json())
            return "NOK"

    # "method": "GET", "url": "https://my.canary.is/api/locations"
    def getLocations(self):
        command= "locations"
        headers={}
        headers["X-XSRF-TOKEN"]=self.xsrf_token
        headers["Cookie"]= "ssesyranac=" + self.session
        headers['Authorization'] = 'Bearer ' + self.accessToken
        response = requests.get(self.baseUrl+command, headers=headers)
        s=response.headers["set-cookie"].split(';')
        for astring in s:
            if "XSRF-TOKEN" in astring:
                self.xsrf_token=astring.split('=')[1]
            if "ssesyranac" in astring:
                self.session=astring.split('=')[1]
        #print(self.xsrf_token)
        #print(self.session)
        return response.json()
    
    # "method": "GET", "url": "https://my.canary.is/api/readings?deviceId=123456&type=canary"
    def getMeasurements(self, deviceId=None, devicetype=None):
        command= "readings"
        headers={}
        headers["X-XSRF-TOKEN"]=self.xsrf_token
        headers["Cookie"]= "ssesyranac=" + self.session
        headers['Authorization'] = 'Bearer ' + self.accessToken
        payload = {}
        payload["deviceId"] = deviceId
        payload["type"] = devicetype
        #print(self.xsrf_token)
        #print(self.session)
        #print(payload)
        response = requests.get("https://my.canary.is/api/readings?deviceId=" + deviceId + "&type=" + devicetype, headers=headers)
        # response = requests.get(self.baseUrl+command, headers=headers, data=payload)
        s=response.headers["set-cookie"].split(';')
        for astring in s:
            if "XSRF-TOKEN" in astring:
                self.xsrf_token=astring.split('=')[1]
            if "ssesyranac" in astring:
                self.session=astring.split('=')[1]
        return response.json()
        
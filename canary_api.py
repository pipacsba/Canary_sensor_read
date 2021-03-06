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
        self.sessiontoken = None

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
            self.UpdateTokenInfo(response.cookies)
            # print("First call with the right content")
            
            # with header information available log in
            if len(self.session)>10:
                headers={}
                headers["X-XSRF-TOKEN"]=self.xsrf_token
                headers["Cookie"]= "ssesyranac=" + self.session
                response = requests.post("https://my.canary.is/api/auth/login", data=payload, headers=headers)
                response.raise_for_status()
                self.UpdateTokenInfo(response.cookies)
                access_token = response.json()["access_token"]
                # print(response.json())
                self.accessToken = access_token
                # print("access token get")
            return "OK"

        except requests.exceptions.HTTPError as error:
            # print('Request Exception:')
            # print(response.request.body )
            # print(response.json())
            return "NOK"

    # "method": "GET", "url": "https://my.canary.is/api/locations"
    def getLocations(self):
        # print("getloaction called")
        command= "locations"
        headers={}
        headers["X-XSRF-TOKEN"]=self.xsrf_token
        headers["Cookie"]= "ssesyranac=" + self.session
        headers['Authorization'] = 'Bearer ' + self.accessToken
        response = requests.get(self.baseUrl+command, headers=headers)
        self.UpdateTokenInfo(response.cookies)
        return response.json()
    
    # "method": "GET", "url": "https://my.canary.is/api/readings?deviceId=1234567&type=canary"
    def getMeasurements(self, deviceId=None, devicetype=None):
        # print("getmeasurements called")
        command= "readings"
        headers={}
        headers["X-XSRF-TOKEN"]=self.xsrf_token
        headers["Cookie"]= "ssesyranac=" + self.session
        headers['Authorization'] = 'Bearer ' + self.accessToken
        payload = {}
        payload["deviceId"] = deviceId
        payload["type"] = devicetype
        response = requests.get("https://my.canary.is/api/readings?deviceId=" + deviceId + "&type=" + devicetype, headers=headers)
        # response = requests.get(self.baseUrl+command, headers=headers, data=payload)
        self.UpdateTokenInfo(response.cookies)
        return response.json()
        
    def UpdateTokenInfo(self, cookiesjar=None):
        if len(cookiesjar)>1:
            # print(cookiesjar)
            self.xsrf_token=cookiesjar['XSRF-TOKEN']
            # print(self.xsrf_token)
            if "ssesyranac" in cookiesjar:
                self.session=cookiesjar['ssesyranac']
                # print(self.session)
            if "ssesyranac:token" in cookiesjar:
                self.sessiontoken=cookiesjar['ssesyranac:token']


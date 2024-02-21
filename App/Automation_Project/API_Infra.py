#Factory Method
import requests as rq
from abc import ABC, abstractmethod
import logging
import json

#Creator
class APICommunicator(ABC):
    #factory method
    @abstractmethod
    def send_request(self):
        pass

    @abstractmethod
    def parse_response(self):
        pass

#concrete creator
class GetWatherAPI(APICommunicator):

    def send_request(self,endpoint,params=None):
        logging.info("initiating request")
        response = rq.get(endpoint,params=params)
        return response.json()

    def parse_response(self, data):
        print(data)

class PostWeatherAPI(APICommunicator):

    def send_request(self,endpoint,params=None,headers=None,data=None):
        logging.info("initiating request")
        response = rq.post(endpoint, params=params,headers=headers,data=data)
        return response.json()

    def parse_response(self, data):
        print(data)

class Communicator:
    def setting_request(self,type):
        if type=="get":
            return GetWatherAPI()
        elif type=="post":
            return PostWeatherAPI()
        else:
            return f"{type} is not valid input"

if __name__=="__main__":
    o1=Communicator()
    url='https://jsonplaceholder.typicode.com/posts'
    parameters={'q':'Mumbai','appid':'8a57ebe7c8311e5b3fa4b407aea78c23'}
    data={"title": "foo","body": "bar","userId": 1}
    headers={'Content-type': 'application/json; charset=UTF-8'}

    getter=o1.setting_request("get")
    getter.parse_response(getter.send_request(url+'/1'))

    poster = o1.setting_request("post")
    poster.parse_response(poster.send_request(url,data=json.dumps(data),headers=headers))



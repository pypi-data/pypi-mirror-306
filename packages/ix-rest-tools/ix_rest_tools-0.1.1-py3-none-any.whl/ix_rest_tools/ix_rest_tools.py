# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 13:54:06 2024

@author: AleksanderHykkerud
"""
# API reference https://www.beijerelectronics.com/docs/iX-251-Reference/en/web-server.html

import requests
import json

def get_tags(url,session):
    result = session.get("http://"+url+"/tags")
    if result.status_code == 200:
        return result.json()
    else:
        return False

def get_value(url,tag,session):
    headers = {'Content-type': "application/json",
               "Accept": "application/json"}
    result = session.get("http://"+url+"/tags/"+tag,headers=headers)

    if result.status_code == 200:
        return result
    else:
        return False

def get_values(url,tags,session,process_values = True):
    url = "http://"+url+"/tagbatch"
    data = {
    "getTags": tags,  # List of tag names to return

    }
    headers = {'Content-type': "application/json",
               "Accept": "application/json"}
    response = session.post(url, json=data,headers=headers)
    
    if response.status_code == 200:
        if process_values:
            values = {}
            for item in response.json()["tags"]:
                values[item["name"]] = item["value"]
            return values
        return response
    else:
        return False




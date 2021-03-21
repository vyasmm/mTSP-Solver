"""
Python launcher for interaction with JS
Created on Fri Feb 28 15:35:08 2020

@author: Mansh
"""

from bottle import hook, response, route, run, static_file, request
import json
import socket
import os
import transportation
import capacitatedVRP
import cap_tm_wndwVRP

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/sampleJSON/<p>/<n>/<c>/<algo>/<manuf>/<distb1>/<distb2>/<distb3>/<distb4>/<distb5>/<distb6>/<distb7>', method='GET')
def mySample(p,n,c,algo,manuf,distb1,distb2,distb3,distb4,distb5,distb6,distb7):
    key = "AIzaSyAxKSw9FJD7o0XQg736WCDfU8u1BqTR7GQ" #Please Specify your GoggleMapsAPI key inside the quotes 
    if(p=="a"):
        return transportation.runMultiVehicleOptimzation(key,int(n),algo,manuf,distb1,distb2,distb3,distb4,distb5,distb6,distb7)
    elif(p=="b"):
        return capacitatedVRP.runCapacitatedVRP(key,int(n),int(c))
    elif(p=="c"):
        return cap_tm_wndwVRP.runCapacitated_TW_VRP(key)

run(host='localhost', port=8080)

import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import urllib2
import datetime
import requests

url = "https://www.fast2sms.com/dev/bulk"
payload = "sender_id=FSTSMS&message=Alert there is fire at home &language=english&route=p&numbers=940***3**3"
headers = {
'authorization': "4vgoDlZ0xrFdzAJOpNh73MqYViIs6WBCcaeKwbPLm52kQyHjuUbj8snEGODCQPRc9mWIqy1aUexgSTit",
'Content-Type': "application/x-www-form-urlencoded",
'Cache-Control': "no-cache",
}

TRUE = 1
FALSE = 0

DEBUG = 1

MQpin = 19
myDelay = 2

FLAG=0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(MQpin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(26,GPIO.OUT)
def getSensorData():
    return (str(GPIO.input(MQpin)))

def main():
    while (True):
        FLAG=0
        GAS = getSensorData()
        LT = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        if GAS=='1':
            GAS="NOT DETECTED"
        else :
            GAS="DETECTED"
            FLAG=1
            
        print (LT + " : " + GAS)
        if FLAG==1:
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text)
            GPIO.output(26, GPIO.HIGH)
            sleep(int(5))
            GPIO.output(26, GPIO.LOW)

        sleep(int(myDelay))

if __name__ == '__main__':
    main()


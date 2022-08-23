# from flask import Flask, request
import base64
import os
import time
# from datafill import *
import cv2
import numpy as np
from PIL import Image
from threading import Event
# from easyocr1 import *
from flask import Flask, render_template, Response, request, session, jsonify
import sqlite3
app = Flask(__name__)
app.debug = False
# @app.route('/')
# def hello_world():
#    return "hello world"
currentlocation = os.path.dirname(os.path.abspath(__file__))
print(currentlocation+'/login.db')
img_data = {'image': "no image", 'langs': 'en', 'gpu': -1}




@app.route('/login', methods=['GET', 'POST'])
def checklogin():
    UN = request.form['username']
    PW = request.form['password']

    sqlconnection = sqlite3.Connection(currentlocation+'/login.db')
    cursor = sqlconnection.cursor()
    # print(cursor)
    query1 = "SELECT Username , Password FROM Users WHERE Username='{un}' AND Password = '{pw}'".format(un=UN,pw=PW)
    rows = cursor.execute(query1)
    rows = rows.fetchall()
    if len(rows) == 1:
        return jsonify({'message': 'valid','code':200})
    else:
        return jsonify({'message': 'notvalid','code':500})

@app.route('/submit_data', methods=['GET','POST'])
def storedata():
    global AADHAR_FRONT,UN,AADHAR_BACK,ROOM_NO,FROM,AMOUNT
    errorsDict = {"errors": {"UN": [], "AADHAR_FRONT": [], "AADHAR_BACK":[] ,"ROOM_NO": [],"FROM": [], "AMOUNT":[]},"received": {"UN": [], "AADHAR_FRONT": [],"AADHAR_BACK":[], "ROOM_NO": [],"FROM": [], "AMOUNT":[]}}
    # messageDict = {"received": {"UN": [], "AADHAR_FRONT": [],"AADHAR_BACK":[], "ROOM_NO": [],"FROM": [], "AMOUNT":[]}}

    try:
        # try:
        UN = request.form['username']
        if UN != "":
            errorsDict["received"]["UN"].append(200)
        else:
            errorsDict["errors"]["UN"].append({"message":"username","code":300})
        # print("user name received ",UN)
        # try:
        AADHAR_FRONT = request.files['front_image']
        print(AADHAR_FRONT)
        print(type(AADHAR_FRONT))
        AADHAR_FRONT.seek(0, os.SEEK_END)
        if AADHAR_FRONT.tell() != 0:
            errorsDict["received"]["AADHAR_FRONT"].append(200)

        else:
            errorsDict["errors"]["AADHAR_FRONT"].append({"message":"AADHAR_FRONT","code":300})
        # try:
        AADHAR_BACK = request.files['back_image']
        AADHAR_BACK.seek(0, os.SEEK_END)
        if AADHAR_BACK.tell() != 0:
            errorsDict["received"]["AADHAR_BACK"].append(200)
        else:
            errorsDict["errors"]["AADHAR_BACK"].append({"message":"AADHAR_BACK","code":300})

        # print(AADHAR_FRONT)
        # try:
        ROOM_NO = request.form['room']
        if ROOM_NO != "":
            errorsDict["received"]["ROOM_NO"].append(200)
        else:
            errorsDict["errors"]["ROOM_NO"].append({"message":"ROOM_NO","code":300})

        # try:
        FROM = request.form['from']
        if FROM !="":
            errorsDict["received"]["FROM"].append(200)
        else:
            errorsDict["errors"]["FROM"].append({"message":"FROM","code":300})

        # try:
        AMOUNT = request.form['amount']
        if AMOUNT !="":
            errorsDict["received"]["AMOUNT"].append(200)
        else:
            errorsDict["errors"]["AMOUNT"].append({"message":"AMOUNT","code":300})
    except:
        return jsonify({"error":400,"message":"key missing"})


    # # print(type(AADHAR_FRONT))
    # img = Image.open(AADHAR_FRONT.stream).save("temp.jpg")
    # time.sleep(2)
    # # print(UN,ROOM_NO,FROM,AMOUNT)
    # img_data['image'] = "temp.jpg"
    # event_trigger = Event
    # # # formfillup = datafillup()
    # # aadhar_val = aadharocr(img_data,currentlocation,UN,ROOM_NO,FROM,AMOUNT,event_trigger)
    # # #
    # # aadhar_val.start()
    # # # t = Thread(target=run)
    # # # t.start()
    # print(len(errorsDict[0].values()))
    return jsonify(errorsDict)


# fillform = datafillup()
# fillform.run()








if __name__ == '__main__':
   # socketio.run(app)
    app.run(host="0.0.0.0")
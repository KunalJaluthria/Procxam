import cv2 as cv
import numpy as np
import face_recognition as fr
import os
import csv
from datetime import datetime
from datetime import date
import sys
from flask import Flask, render_template, request, url_for, redirect
import pandas as pd

# Function for finding the face encodings
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# For creating new csv file for test attendance based on date
def createtestfile():
    today = date.today()
    d1 = today.strftime("%d-%m-%Y")
    file = open(sys.path[0]+"/TestAttendance/"+d1+".csv",'a+')
    file.writelines(f'{"Name"},{"Email"},{"Time"},{"TestId"},{"Attendence"}')
    file.close()

# For marking test attendance after verification in csv file
def markAttendance(name,Email,id):
    today = date.today()
    d1 = today.strftime("%d-%m-%Y")
    d2 = d1+".csv"
    p = "Present"
    if (os.path.isfile(sys.path[0]+"/TestAttendance/"+d2) == False):
        createtestfile()
    with open(sys.path[0]+"/TestAttendance/"+d2, 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{Email},{dtString},{id},{p}')

# For creating new csv file for meeting attendance based on date
def createmeetfile():
    today = date.today()
    d1 = today.strftime("%d-%m-%Y")
    file = open(sys.path[0]+"/MeetAttendance/"+d1+".csv",'a+')
    file.writelines(f'{"Name"},{"Time"},{"Attendence"}')
    file.close()

# For marking test attendance after verification in csv file
def markMeetAttendance(name):
    today = date.today()
    d1 = today.strftime("%d-%m-%Y")
    d2 = d1+".csv"
    p = "Present"
    if (os.path.isfile(sys.path[0]+"/MeetAttendance/"+d2) == False):
        createmeetfile()
    with open(sys.path[0]+"/MeetAttendance/"+d2,'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString},{p}')

# For verifying the user image in the Train_img folder if it exists. (Test Verification)
def Face_recog(Email):
    path = 'Train_img'
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)
    
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    img = cv.imread(sys.path[0]+"/Image.png", 1)
    imgS = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    facesCurFrame = fr.face_locations(imgS)
    encodesCurFrame = fr.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = fr.compare_faces(encodeListKnown, encodeFace)
        faceDis = fr.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            return name
        else:
            return "Unknown"
    
    return "Face cannot be indentified"

# For verifying the user's face id before login.
def Face_verification(username):
    path = 'Registered User'
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)
    
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    img = cv.imread(sys.path[0]+"/Image_Verf.png", 1)
    imgS = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    facesCurFrame = fr.face_locations(imgS)
    encodesCurFrame = fr.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = fr.compare_faces(encodeListKnown, encodeFace)
        faceDis = fr.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            matchuser = username.upper()
            if(name == matchuser):
                return "Verfication done successfully"
            else:
                return "Entered username doesn't match"
        else:
            return "User record not found"
    
    return "Face cannot be indentified"

# For marking the attendance of the attendees in online meeting.
def Attendance():
    path = 'Train_img'
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)
    
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    img = cv.imread(sys.path[0]+"/Attendance_Image.png", 1)
    imgS = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    facesCurFrame = fr.face_locations(imgS)
    encodesCurFrame = fr.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = fr.compare_faces(encodeListKnown, encodeFace)
        faceDis = fr.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            markMeetAttendance(name)
            return name
        else:
            return "Unknown"
    
    return "Face cannot be indentified"

# For checking the Face id of the new user before registering in the Registered User folder.
def Register_Check():
    path = 'Registered User'
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)
    
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    img = cv.imread(sys.path[0]+"/Verify.png", 1)
    imgS = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    facesCurFrame = fr.face_locations(imgS)
    encodesCurFrame = fr.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = fr.compare_faces(encodeListKnown, encodeFace)
        faceDis = fr.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            return "User record already exists!"
        else:
            return "User record not found"

    return "Face cannot be indentified"
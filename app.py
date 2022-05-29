from asyncio.log import logger
import base64
from base64 import b64encode, b64decode
from encodings import utf_8
from pydoc import classname
import face_recognition as fr
import io
import os
import sys
from posixpath import split
import cv2 as cv
import numpy as np
from distutils.log import debug
from email.mime import image
from io import BytesIO
import re
import PIL.Image as Image
from flask import Flask, render_template, request, url_for, redirect, Response, flash, session
from Face_recognition import Attendance, Face_recog, Face_verification, findEncodings, markAttendance, Register_Check
from datetime import datetime
import sqlite3
app = Flask(__name__)
app.secret_key = "Kunal123"

# Commands for Creating the User Details Table in the Info database
# con = sqlite3.connect("Info.db")
# c = con.cursor()
# c.execute("CREATE TABLE User(Username TEXT, Password TEXT)")
# c.execute("DELETE FROM User")
# con.commit()
# con.close()

# Commands for Creating the Test Link Table in the Info database
# con = sqlite3.connect("Info.db")
# c = con.cursor()
# c.execute("CREATE TABLE Links(Id INTEGER PRIMARY KEY AUTOINCREMENT, Assessment_Name TEXT, Teacher_Name TEXT, Subject TEXT, Link TEXT, Gen_link TEXT)")
# c.execute("DELETE FROM Links")
# c.execute("INSERT INTO Links (Assessment_Name,Teacher_Name,Subject,Link,Gen_link) VALUES('Class Test 1','Kunal', 'Data Structures', 'https://docs.google.com/forms/d/e/1FAIpQLSdr5cS2dGy70Uuf6aL_AIhRCrzCr6I7xyEOXMe9Eb_dspqmyw/viewform?embedded=true', 'http://127.0.0.1:5000/test/1')")
# con.commit()
# con.close()

# For rendering index.html template
@app.route("/")
def index():
    if session.get("loggedin", None) is None:
        session["loggedin"] = False
    return render_template('index.html')

# For inserting the generated test link in the Links Table in Info.db database
@app.route("/SaveLink", methods=["GET","POST"])
def SaveLink():
    if(request.method == "POST"):
            name = request.form.get("Aname")
            Tname = request.form.get("tname")
            subject = request.form.get("subject")
            formlink = request.form.get("formlink")
            con = sqlite3.connect("Info.db")
            c = con.cursor()
            c.execute("SELECT COUNT(*) AS Ct FROM Links WHERE Link = '"+formlink+"'")
            db_result=c.fetchone()[0]
            if db_result==0:
                c.execute("SELECT Id AS Data FROM Links ORDER BY Id DESC LIMIT 1")
                r = c.fetchall()
                for i in r:
                    Idd = i[0]
                    dat = str(Idd+1)
                    print(dat)
                    genlink = "http://127.0.0.1:5000/test/"+dat

                p = (name,Tname,subject,formlink,genlink)
                c.execute("INSERT INTO Links (Assessment_Name,Teacher_Name,Subject,Link,Gen_link) VALUES(?,?,?,?,?)", p)
                con.commit()
                con.close()
                return genlink
            else:
                con.commit()
                con.close()
                return "Link already exists!"

# For rendering Log_Reg.html template
@app.route("/Log_Reg")
def Log_Reg():
    return render_template('Log_Reg.html')

# For rendering JoinMeeting.html template
@app.route("/JoinMeeting")
def JoinMeeting():
    return render_template('JoinMeeting.html')

# For marking attendance of the attendees using face recognition
@app.route("/markattendance", methods=["GET","POST"])
def markattendance():
    if request.method == "GET":
        return "Snapshot not received"
    elif request.method == "POST":
        imagg = request.form.get("content")
        image_data = str(imagg)
        with open("Attendance_Image.png","wb") as f:
            f.write(base64.b64decode(image_data))
        value = Attendance()
        if(value!="Unknown" and value!="Face cannot be indentified"):
            return "Hi! "+value+", Enjoy your meeting."
        else:   
            return "User cannot be indentified. Try Again!"

# For getting the url for google forms page
@app.route("/geturl", methods=["GET","POST"])
def geturl():
    if(request.method == "POST"):
        url = request.form.get("link")
        con = sqlite3.connect("Info.db")
        c = con.cursor()
        c.execute("SELECT Link AS Ct FROM Links WHERE Gen_link = '"+url+"'")
        r = c.fetchall()
        for i in r:
            link = i[0]
            con.commit()
            con.close()
            return link

# For rendering Test.html template if id exists
@app.route("/test/<id>")
def test(id):
    dat = str(id)
    chlink = "http://127.0.0.1:5000/test/"+dat
    con = sqlite3.connect("Info.db")
    c = con.cursor()
    c.execute("SELECT COUNT(*) AS Ct FROM Links WHERE Gen_link = '"+chlink+"'")
    db_result=c.fetchone()[0]
    if (db_result==0):
        con.commit()
        con.close()
        return render_template('404.html')
    else:
        con.commit()
        con.close()
        return render_template('Test.html')

# For rendering Login.html template
@app.route("/Login")
def Login():
    return render_template('Login.html')

# For rendering CreateTest.html template
@app.route("/CreateTest")
def CreateTest():
    return render_template('CreateTest.html')

# For rendering Meet.html template
@app.route("/meet")
def Meet():
    return render_template('Meet.html')

# For checking the record of the user in User Table in Info.db database
@app.route("/UserCheck", methods=["GET","POST"])
def UserCheck():
    if(request.method == "POST"):
        if(request.form.get("username") != "" or request.form.get("password") != ""):
            username = request.form.get("username")
            password = request.form.get("password")
            con = sqlite3.connect("Info.db")
            c = con.cursor()
            c.execute("SELECT * FROM User Where Username = '"+username+"' and Password = '"+password+"'")
            r = c.fetchall()
            for i in r:
                if(username == i[0] and password == i[1]):
                    session["loggedin"] = True
                    return "Logged In Successfully!"
            else:
                session["loggedin"] = False
                return "Invalid Username or Password!"

# For clearing the session and redirect to index.html
@app.route("/Logout")
def logout():
    session["loggedin"] = False
    return redirect(url_for('index'))

# For checking if user is logged-in or not.
@app.route("/checklogin", methods=["GET","POST"])
def checklogin():
    if(request.method == "POST"):
        if(session["loggedin"] == True):
            return "user"
        else:
            return "User is not logged in!"

# For registering a new user
@app.route("/Register", methods=["GET","POST"])
def Register():
    if(request.method == "POST"):
        if(request.form.get("usern")!="" and request.form.get("pass")!="" and request.form.get("cnfPass")!=""):
            username = request.form.get("usern")
            password = request.form.get("pass")
            cnfpassword = request.form.get("cnfPass")
            if(password == cnfpassword):
                con = sqlite3.connect("Info.db")
                c = con.cursor()
                c.execute("SELECT COUNT(*) AS Ct FROM User WHERE Username = '"+username+"'")
                db_result=c.fetchone()[0]
                if db_result==0:
                    c.execute("INSERT INTO User VALUES('"+username+"', '"+password+"')")
                    con.commit()
                    con.close()
                    return "Registration is Successfull!"
                else:
                    return "User is already registered!"
            else:
                return "Passwords doesn't match!"
    return render_template('Register.html')

# Getting the image from javascript using post request and then verifying the image
@app.route("/api", methods=["GET","POST"])
def api():
    if request.method == "GET":
        return "Snapshot not received"
    elif request.method == "POST":
        text = request.form.get("email")
        imagg = request.form.get("content")
        image_data = str(imagg)
        img_name = "{}.png".format(text)
        with open("Image.png","wb") as f:
            f.write(base64.b64decode(image_data))
        value = Face_recog(text)
        if(value != "Unknown" and value!= "Face cannot be indentified"):
            with open(sys.path[0]+"/TestBackup/"+img_name,"wb") as f:
                f.write(base64.b64decode(image_data))
        return value

# For checking if the Face Id of user already exist or not. (For preventing creation of multiple accounts)
@app.route("/snap", methods=["GET","POST"])
def snap():
    if request.method == "GET":
        return "Snapshot not received"
    elif request.method == "POST":
        if(request.form.get("username")!="" and request.form.get("password")!="" and request.form.get("cnfPassword")!=""):
            username = request.form.get("username")
            password = request.form.get("password")
            cnfpassword = request.form.get("cnfPassword")
            if(password == cnfpassword):
                con = sqlite3.connect("Info.db")
                c = con.cursor()
                c.execute("SELECT COUNT(*) AS Ct FROM User WHERE Username = '"+username+"'")
                db_result=c.fetchone()[0]
                if db_result==0:
                    imagg = request.form.get("content")
                    image_data = str(imagg)
                    with open("Verify.png","wb") as f:
                        f.write(base64.b64decode(image_data))
                    value = Register_Check()
                    if(value=="User record not found"):
                        img_name = "{}.png".format(username)
                        with open(sys.path[0]+"/Registered User/"+img_name,"wb") as f:
                            f.write(base64.b64decode(image_data))
                        with open(sys.path[0]+"/Train_img/"+img_name,"wb") as f:
                            f.write(base64.b64decode(image_data))
                        con.commit()
                        con.close()
                        return "Face Id registered successfully"
                    elif(value=="Face cannot be indentified"):
                        return "Face cannot be detected!"
                    else:
                        return "Face Id registered with another account!"
                else:
                    return "User is already registered!"
            else:
                return "Passwords doesn't match! Try Again"
        else:
            return "Input field is empty!"

# For marking the attendance in the TestAttendance folder
@app.route("/mark_attendance", methods=["GET","POST"])
def Mark_Attendance():
    if request.method == "GET":
        return "System cannot mark the attendance!"
    elif request.method == "POST":
        id = request.form.get("id")
        name = request.form.get("name")
        text = request.form.get("email")
        markAttendance(name,text,id) 
        return "Attendance Marked!"

# For verifying the Face Id of the user before login using username.
@app.route("/faceidverf", methods=["GET","POST"])
def faceidverf():
    if request.method == "GET":
        return "Snapshot not received"
    elif request.method == "POST":
        if(request.form.get("username")!="" and request.form.get("pass")!=""):
            username = request.form.get("username")
            imag = request.form.get("content")
            image_data = str(imag)
            with open("Image_Verf.png","wb") as f:
                f.write(base64.b64decode(image_data))
            value = Face_verification(username)
            return value
        else:
            return "Input field empty!"

if __name__ == "__main__":
    app.run(debug=True)
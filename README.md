# PROCXAM

## MICROSOFT ENGAGE 2022 PROJECT

<p align="center"><img src="static/images/logo.png" width="200" height="200"></p>

## Description
During the Covid-19 pandemic, There was a new phase of conducting tests, assessments, and meetings online by schools and universities. Teachers faced many problems in conducting online tests and meetings securely and maintaining attendance such that there is no proxy of the students. It was challenging to maintain the decorum and integrity of the test and meet online mode. So, For the solution to this problem, I have developed Procxam.

Procxam is a face-recognition-based website for managing and tracking attendance, preventing the proxy in online tests and meetings. It helps teachers to conduct online tests and meetings more efficiently and securely. It uses face recognition technology to verify the student's authenticity by capturing real-time images and checking them in the record. Procxam helps maintain the test and meeting integrity and make it more secure through the face recognition technology while assuring that the students experience is exceptional at each step.

This project is developed as a part of the Microsoft Engage 2022 Program. It was a wonderful experience and an insightful journey with a lot of learning.
## Video Demo Link

https://drive.google.com/file/d/1kPDBURb7X4RN3FwQcrXCByH-YKvaUdAV/view?usp=sharing
## Features

1. Registration functionality with additional Face Id.
2. Storing registered user data in the database.
3. Storing registered Face Id in the Registered User folder.
4. Prevent the creation of duplicate accounts for the already registered user.
5. Login functionality with additional Face Id verification/authentication.
6. Perform face detection before registering and verifying the Face Id.
7. Hosting google forms tests having Face id verification.
8. Generating test links with unique IDs and saving them to the database.
9. Check the link id in the database before loading the URL.
10. Verifying the student's identity using face recognition and recording attendance with time.
11. Host online meets with an automated attendance tracker.
12. Verifying and marking students' attendance before allowing entry into the meet.
13. Giving access only to the verified users to the meeting.
14. Generating new CSV files and keeping track of attendance based on the current date.
## Technologies Used

### 1. Languages Used
- HTML
- CSS
- JavaScript
- Python 3.10.4
- Flask
- AJAX
- JQuery

### 2. Database Used
SQLite Database

### 3. API Used
Video SDK API (Video call and chat application)

API Key (Already entered in source code):- a20da4e5-2062-4792-8d2b-cdd68783a75a

If the above API Key doesn't work, Create an API Key from https://www.videosdk.live/ and enter it in the API Key in the Script section of /templates/Meet.html

### 4. Python library used for Face recognition
- OpenCV
- face-recognition 1.3.0
## Installation and Deployment

1. Clone the Github repository into a folder and open the folder in Visual studio code.
```bash
$ git clone git@github.com:KunalJaluthria/Procxam.git
```

2. In the folder, Set up the Virtual environment.
```bash
$ pip install virtualenv
$ virtualenv env
```

3. If any error comes while setting up the Virtual environment. Then, open the Window powershell as Administrator and Set ExecutionPolicy unrestricted. If no error in shown, skip this step and move to 4th step.
```bash
$ Set-ExecutionPolicy unrestricted
```

4. Activate the Virtual environment.
```bash
$ .\env\Scripts\activate.ps1
```

5. Install packages and libraries in the virtual env.
```bash
(env) $ pip install -r requirements.txt
```

6. Run the project on the server.
```bash
(env) $ python .\app.py
```
Once installation setup is complete and the server starts running, use http://127.0.0.1:5000 to visit the Procxam website.
## Additional Information

Demo Google form link for generating the test link for hosting a test(To be pasted in Google form link textbox): https://docs.google.com/forms/d/e/1FAIpQLSdJpZeGXbOUQjLCZ62YHGw4kshz6xnqMrqx4Hi03uAILdOglg/viewform?usp=sf_link

For viewing the tables, attributes, and records in the SQLite database. Use this link,
https://inloop.github.io/sqlite-viewer/

The Python version used for developing the project is 3.10.4

For viewing the attendance record, check the TestAttendance and MeetAttendance folders, respectively. The CSV file gets created automatically based on the current date.
## Screenshots

### 1. Homepage
<p align="center"><img src="/Screenshots/PROCXAM.png" width="750" height="1100"></p>

### 2. Login/Register Page
<p align="center"><img src="/Screenshots/2.jpg" width="750" height="420"></p>

### 3. Register Page
<p align="center"><img src="/Screenshots/3.jpg" width="750" height="420"></p>

<p align="center"><img src="/Screenshots/4.jpg" width="750" height="420"></p>

<p align="center"><img src="/Screenshots/5.jpg" width="750" height="420"></p>

<p align="center"><img src="/Screenshots/6.jpg" width="750" height="420"></p>

<p align="center"><img src="/Screenshots/7.jpg" width="750" height="420"></p>

- If the user is already registered and try to register using different credentials. Then, Face Id detects the user and prevents from creating new account.

<p align="center"><img src="/Screenshots/8.jpg" width="750" height="420"></p>

### 3. Login Page
<p align="center"><img src="/Screenshots/9.jpg" width="750" height="420"></p>

<p align="center"><img src="/Screenshots/10.jpg" width="750" height="420"></p>

<p align="center"><img src="/Screenshots/11.jpg" width="750" height="420"></p>

### 3. Hosting a test(Generating the test link)
<p align="center"><img src="/Screenshots/13.jpg" width="750" height="420"></p>

### 4. Test link with Face-id verification
<p align="center"><img src="/Screenshots/14.jpg" width="750" height="420"></p>

<p align="center"><img src="/Screenshots/15.jpg" width="750" height="420"></p>

<p align="center"><img src="/Screenshots/16.jpg" width="750" height="420"></p>

### 5. 404 Error page in case the test link doesn't exists.
<p align="center"><img src="/Screenshots/17.jpg" width="750" height="420"></p>

### 6. Hosting a Video Meeting
- Host Page
<p align="center"><img src="/Screenshots/19.jpg" width="750" height="420"></p>

- Attendee page

First the attendance is recorded. Only the verified attendee will be redirected to the meeting page.
<p align="center"><img src="/Screenshots/20.jpg" width="750" height="420"></p>

<p align="center"><img src="/Screenshots/21.jpg" width="750" height="420"></p>

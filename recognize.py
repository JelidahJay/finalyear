import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pymysql
import mysql.connector

path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

print(classNames)

# def markAttendance(name):
#     with open('Attendance.csv','r+') as f:
#         myDataList = f.readlines()
#         print(myDataList)
#         nameList = []
#         for line in myDataList:
#             entry = line.split(',')
#             nameList.append(entry[0])
#         if name not in nameList:
#             now = datetime.now()
#             dtString = now.strftime('%H:%M:%S')
#             f.writelines(f'\n{name},{dtString}')

# markAttendance()


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

encodeListKnown = findEncodings(images)
print('encoding complete')

def markAttendance(Event,name,Status,date,time):
    conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "dbattendance")
    cur = conn.cursor()

    sql = ''' insert into sanction(Eventname,StudentName,Status,date,time) values (%s,%s,%s,%s,%s)'''

    val=(Event,name,Status,date,time)
    cur.execute(sql,val)
    conn.commit()

def markAttendances(Events,name,Stat,date,time):
    conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "dbattendance")
    cur = conn.cursor()

    sql = ''' insert into sanction(Eventname,StudentName,Status,date,time) values (%s,%s,%s,%s,%s)'''

    val=(Events,name,Stat,date,time)
    cur.execute(sql,val)
    conn.commit()


cap = cv2.VideoCapture(0)
nm = 'a'
while True:
 
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0), None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceloc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        #Display a bounding box around face
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1,x2,y2,x1 = faceloc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            #markAttendance(name) 
            crTime=datetime.now().time()
            crDate = datetime.now().date()
            Event = 'csc4130'
            Status = 'in'
            conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "dbattendance")
            cur2 = conn.cursor()
            cur2.execute("select firstname from student WHERE firstname='%s'  " %name)
            records1 = cur2.fetchall()
            if records1:
                markAttendance(Event,name,Status,str(crDate),str(crTime))
                
            
            else:
                
                crTime1=datetime.now().time()
                crDate1 = datetime.now().date()
                Events = 'csc4130'
                Stat = 'out'
                markAttendances(Events,name,Stat,str(crDate),str(crTime))
                # conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "dbattendance")
                # cur1 = conn.cursor()

                # sql = ''' insert into sanction(Eventname,StudentName,Status,date,time) values (%s,%s,%s,%s,%s)'''

                # val=(Events,name,Stat,str(crDate),str(crTime))
                # cur1.execute(sql,val)
                # conn.commit()

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
    # cv2.imshow('Webcam', img)
    # cv2.waitKey(1)
        


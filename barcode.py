from tkinter import*
try:
    import Tkinter as tk
except:
    import tkinter as tk       #import the gui(graphical user interface)
import os
from datetime import datetime
import sys
import random
import sqlite3  #import database sqlite3, it save the barcode to this database
import time
import pymysql

# import RPi.GPIO as GPIO  
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(2, GPIO.OUT) # servo motor
# GPIO.setwarnings(False)

# p = GPIO.PWM(2, 50) # GPIO 2 for PWM with 50Hz
# p.start(8.5) 

print("****************************************START*****************************************************")


root = Tk()
root.title('smart library')
lbl=Label(root,text ="SMART DOOR LOCK SYSTEM",fg ='black' , font =("times new roman", 90),bg='white')
lbl.place(x=100,y=10) #x,y are the position of text

lbl3=Label(root,text ="Developed By",fg ='black' , font =("times new roman", 40),bg='white')
lbl3.place(x=30,y=700)

lbl3=Label(root,text ="Mr. Niraj Kumar",fg ='black' , font =("times new roman", 40),bg='white')
lbl3.place(x=30,y=760)


large_font=('Verdana',40)
ID = Entry(root,width=12,font=large_font) #it create the box
ID .grid(row=4, column=2)
ID .place(x=250,y=250)
ID.focus()

txt  = "Scan ID"
lbl6=Label(root,fg ='red' , font =("times new roman", 50),bg='white')
lbl6.place(x=100,y=100)

def labelconfig():
     p=txt
     color = '#'+("%09x" % random.randint(0,0xFFFFFF))
     lbl6.config(text=p,fg=str(color))
     root.after(200,labelconfig)
labelconfig()      # this funcion change the colour of text

root.geometry('1000x768')
root['bg'] = 'white'  #background color



def fg():
                                            try:
                                                        large_font=('Verdana',20)
                                                        gk=code
                                                        global ID
                                                        coll_id=gk
                                                        ID.delete(0, END)
                                                        ID.insert(0,gk)
                                                        
                                                        conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "dbattendance")
                                                        cur = conn.cursor()
                                                        cur.execute("select * from student_barcode WHERE barcode='%s'  " %ID.get())
                                                       
                                                        records1 = cur.fetchall()
                                                        print_records= ' '
                       
                                                        global ff
                                                        global jj
                                                        ID.delete(0, END)
                                                        row=["Empty","Empty"]
                                                        for row in records1:
                                                                
                                                                ff=row[0]  ###### college id
                                                                jj=row[1]  ##### name
                                                                                                                               
                                                        conn.commit()
                                                        conn.close()
                                                        ID.delete(0, END)                                                       
                                                        if (row[0]=='Empty'):   #if data not match to the barcode,door is close                        
                                                                  large_font=('Verdana',20)                                                                 
                                                                  txt='           Error In Matching Unidentified User            '
                                                                  lbl6=Label(root,fg ='red' , font =("times new roman", 50),bg='white')
                                                                  lbl6.place(x=400,y=500)
                                                                  
                                                                  ID.delete(0, END)
                                                                  print("door close")
                                                                #   p.start(8.5)        ############## motor close the door
                                                                   
                                                                  def labelconfig():
                                                                     p=txt
                                                                     color = '#'+("%06x" % random.randint(0,0xFFFFFF))
                                                                     lbl6.config(text=p,fg=str(color))
                                                                     root.after(300,labelconfig)
                                                                  labelconfig()
                                                        else:       
                                                                 #otherwise door is open

                                                                  large_font=('Verdana',20)                                                             
                                                                  txt='           Correct Matching, Identified User                          '
                                                                  lbl6=Label(root,fg ='red' , font =("times new roman", 50),bg='white')
                                                                  lbl6.place(x=400,y=500)
                                                                  ID.delete(0, END)

                                                                  
                                                                  



                                                                  #p.ChangeDutyCycle(6.6)  ############## motor open the door
                                                                #   time.sleep(0.5)
                                                                  # print("open")
                                                                  def labelconfig():
                                                                     p=txt
                                                                     color = '#'+("%06x" % random.randint(0,0xFFFFFF))
                                                                     lbl6.config(text=p,fg=str(color))
                                                                     root.after(300,labelconfig)
                                                                  labelconfig()

                                                                  
                                                                  import recognize
                                                                  
                                            except Exception as e:
                                             print('Operation failed!')
                                             print('Exception message: ' + str(e))      

def get_key(event):    # it insert the barcode to box,so it compare with database 
    global code
    if event.char in '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM':
       code += event.char

    elif event.keysym == 'Return':
        #print('result:', code)
        fg()           # call the fg() function 
        code=""
code = ''                        
root.bind('<Key>', get_key)

root.mainloop()

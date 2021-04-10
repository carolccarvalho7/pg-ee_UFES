####################################################################################################
##                                 ONO INTERFACE
## Copyright (C) 2017 UFES.
##
## This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
## 
## Maintainers: Andres Ramirez
##              Carolina Carvalho
##
## Laboratorio de Automacao Inteligente - LAI 4
####################################################################################################

#!/usr/bin/python

import time
import logging
#import tornado
#import tornado.escape
#import tornado.ioloop
#import tornado.options
#import tornado.web
#import tornado.websocket
#import tornado.httpclient
import os.path
import uuid
import urllib
import requests
import threading

#import httplib_fork as httplib
from websocket import create_connection

from tornado import gen 

from Tkinter import *

token_com = None
s = requests.Session()

####################################################################################################
##                              WEBSOCKET
#################################################################################################### 
def ws_com(command):
    ws = create_connection("ws://192.168.42.1:80/sockjs/websocket")
    data = {'action': 'authenticate', 'token': token_com}
    json_data= tornado.escape.json_encode(data)
    json_command= tornado.escape.json_encode(command)
    print "Sending 'authentication'..."
    ws.send(json_data)
    print "Sending 'command'..."
    ws.send(json_command)
    ws.close()

####################################################################################################
##                              TAREFAS
####################################################################################################        
def oi():
    sw.Start()
    r_app = s.get('http://192.168.42.1/openapp/circumplex')

    payload = {'pin_number': 13, 'value': 1460}
    r_eye = s.get('http://192.168.42.1/robot/servo/', data=payload)
    payload = {'pin_number': 10, 'value': 1600}
    r_eye = s.get('http://192.168.42.1/robot/servo/', data=payload)
    
    payload = {'pin_number': 3, 'value': 1555}
    r_eye = s.get('http://192.168.42.1/robot/servo/', data=payload)
    payload = {'pin_number': 2, 'value': 1660}
    r_eye = s.get('http://192.168.42.1/robot/servo/', data=payload)

    r_eye = s.get('http://192.168.42.1/robot/dof/', data=payload)

    payload_s = {'s': 'nome_ono.wav'}
    r_sound = s.get('http://192.168.42.1/robot/sound/', params=payload_s)
    
    payload = {'channel': 0, 'pos': 1500, 'prompt': 14 }
    r_arm = s.post('http://192.168.42.1/robot/arm/', data=payload)
     
    time.sleep(1)

    payload = {'channel': 0, 'pos': 1500, 'prompt': 2 }
    r_arm = s.post('http://192.168.42.1/robot/arm/', data=payload) 
    
def fala(value_rph = 1555, value_rpv = 1660, value_lph = 1460, value_lpv = 1600, audio = "", emo = 0, prompt_1 = 2, prompt_2 = 8):

    emotion(emo) 
    
    payload = {'pin_number': 3, 'value': '%d' %value_rph} #value_rph
    r_eye = s.get('http://192.168.42.1/robot/servo/', data=payload)
    payload = {'pin_number': 2, 'value': '%d' %value_rpv} #value_rpv
    r_eye = s.get('http://192.168.42.1/robot/servo/', data=payload)
    
    
    payload = {'pin_number': 13, 'value': '%d' %value_lph} #value_lph
    r_eye = s.get('http://192.168.42.1/robot/servo/', data=payload)
    payload = {'pin_number': 10, 'value': '%d' %value_lpv} #value_lpv
    r_eye = s.get('http://192.168.42.1/robot/servo/', data=payload)
    
    #time.sleep(1)
    
    som(audio)
    
    #time.sleep(1.5)
    
    payload = {'channel': 0, 'pos': 1500, 'prompt': '%d' %prompt_1}
    r_arm = s.post('http://192.168.42.1/robot/arm/', data=payload)
    payload = {'channel': 0, 'pos': 1500, 'prompt': '%d' %prompt_2}
    r_arm = s.post('http://192.168.42.1/robot/arm/', data=payload)
    
    
    #time.sleep(2)
    r_clapp = s.get('http://192.168.42.1/closeapp')         
    
def som(audio):
    payload_s = {'s': '%s' %audio}
    r_sound = s.get('http://192.168.42.1/robot/sound/', params=payload_s)
    
def emotion(phi):
    payload = {'r': 1.0, 'phi': '%f' %phi, 'time': -1.0}
    r_emo = s.post('http://192.168.42.1/robot/emotion/', data=payload)
    
####################################################################################################
##                              MAIN
####################################################################################################                     
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    payload = {'password': 'opsoro123'}
    r = s.post('http://192.168.42.1/login/', data=payload)
    r_token = s.get('http://192.168.42.1/sockjstoken') 
    token_com = r_token.text   
    
    robot_GUI = Tk()
    robot_GUI.geometry("640x700")
    robot_GUI.wm_title('Robot_GUI - Controle do robo social ONO')
    
    payload = {'pin_number': 13, 'value': 1460}
    r_eye = s.get('http://192.168.42.1/robot/servo/', data=payload)
    payload = {'pin_number': 10, 'value': 1600}
    r_eye = s.get('http://192.168.42.1/robot/servo/', data=payload)
    
    payload = {'pin_number': 3, 'value': 1555}
    r_eye = s.get('http://192.168.42.1/robot/servo/', data=payload)
    payload = {'pin_number': 2, 'value': 1660}
    r_eye = s.get('http://192.168.42.1/robot/servo/', data=payload)
    
    Label(robot_GUI, text = "FALAS PARA APROXIMAR A CRIANCA DO ROBO").place(x=180, y=5)
    B_APRESENTACAO_1 = Button(robot_GUI,
                              text ="APRESENTACAO 1",
                              command = lambda: fala(1824, 1851, 1860, 1500, "ono.wav", 18.5, 14)).place(x=20, y=30)
    A1 = Canvas(robot_GUI, highlightthickness=0)
    A1.place(x=180, y=35)
    A1.create_line(0, 10, 50, 10, arrow="last", width=3, arrowshape=(10, 12, 5))  
                
    B_APRESENTACAO_2 = Button(robot_GUI,
                              text ="APRESENTACAO 2",
                              command = lambda: fala(1824, 1851, 1860, 1500, "robo.wav", 18.5, 2)).place(x=250, y=30)
    A2 = Canvas(robot_GUI, highlightthickness=0)
    A2.place(x=410, y=35)
    A2.create_line(0, 10, 50, 10, arrow="last", width=3, arrowshape=(10, 12, 5))
    
    B_APRESENTACAO_3 = Button(robot_GUI,
                              text ="APRESENTACAO 3",
                              command = lambda: fala(1824, 1851, 1860, 1500, "amigo.wav", 18.5)).place(x=480, y=30)                                       
    f=Frame(robot_GUI, height=2 , width=640, bg="black")
    f.place(x=0, y=70)
                                                                                                                           
    ################################################################################################
    Label(robot_GUI, text = "TAREFA 1 (OLHAR + FALAR)").place(x=250, y=80)
    B1_TAREFA_1 = Button(robot_GUI,
                         text ="INTRODUCAO",
                         command = lambda: fala(1824, 1851, 1860, 1500,"sala_divertida.wav",7)).place(x=20, y=105)                            
    A3 = Canvas(robot_GUI, highlightthickness=0)
    A3.place(x=140, y=110)
    A3.create_line(0, 10, 50, 10, arrow="last", width=3, arrowshape=(10, 12, 5))
    
    B2_TAREFA_1 = Button(robot_GUI,
                         text ="OBJETO 1",
                         command = lambda: fala(1059, 1356, 843, 1851,"Helicoptero.wav",7)).place(x=200, y=105)
    A4 = Canvas(robot_GUI, highlightthickness=0)
    A4.place(x=300, y=110)
    A4.create_line(0, 10, 50, 10, arrow="last", width=3, arrowshape=(10, 12, 5))
    A4 = Canvas(robot_GUI, highlightthickness=0)
    A4.place(x=230, y=140)
    A4.create_line(10, 0, 10, 30, arrow="last", width=3, arrowshape=(10, 12, 5))
    B2_TAREFA_1 = Button(robot_GUI,
                         text ="DE NOVO",
                         command = lambda: fala(1059, 1356, 843, 1851, "Helicoptero.wav",7)).place(x=200, y=175)
                              
    B3_TAREFA_1 = Button(robot_GUI,
                         text ="OBJETO 2",
                         command = lambda: fala(1149, 1446, 1203, 1851, "Caminhao.wav",7)).place(x=365, y=105)
    A5 = Canvas(robot_GUI, highlightthickness=0)
    A5.place(x=465, y=110)
    A5.create_line(0, 10, 50, 10, arrow="last", width=3, arrowshape=(10, 12, 5))
    A5 = Canvas(robot_GUI, highlightthickness=0)
    A5.place(x=400, y=140)
    A5.create_line(10, 0, 10, 30, arrow="last", width=3, arrowshape=(10, 12, 5))
    B3_TAREFA_1 = Button(robot_GUI,
                         text ="DE NOVO",
                         command = lambda: fala(1330, 1446, 1203, 1851, "Caminhao.wav",7)).place(x=370, y=175)
                                  
    B4_TAREFA_1 = Button(robot_GUI,
                         text ="OBJETO 3",
                         command = lambda: fala(1660, 1302, 1460, 2040, "Trem.wav",7)).place(x=530, y=105)
    A6 = Canvas(robot_GUI, highlightthickness=0)
    A6.place(x=565, y=140)
    A6.create_line(10, 0, 10, 30, arrow="last", width=3, arrowshape=(10, 12, 5))
    B3_TAREFA_1 = Button(robot_GUI,
                              text ="DE NOVO",
                              command = lambda: fala(1660, 1302, 1460, 2040, "Trem.wav",7)).place(x=530, y=175)
                              
    f=Frame(robot_GUI, height=2 , width=640, bg="black")
    f.place(x=0, y=215)
    ################################################################################################
    Label(robot_GUI, text = "TAREFA 2 (OLHAR + APONTAR)").place(x=220, y=225)

    B1_TAREFA_2 = Button(robot_GUI,
                         text ="INTRODUCAO",
                         command = lambda: fala(1824, 1851, 1860, 1500,"olhar_apontar.wav",7)).place(x=20, y=250)                            
    A = Canvas(robot_GUI, highlightthickness=0)
    A.place(x=140, y=255)
    A.create_line(0, 10, 50, 10, arrow="last", width=3, arrowshape=(10, 12, 5)) 
    
    B2_TAREFA_2 = Button(robot_GUI,
                         text ="OBJETO 1",
                         command = lambda: fala(1059, 1356, 843, 1851, "", 7, 2,11)).place(x=200, y=250)
    A4 = Canvas(robot_GUI, highlightthickness=0)
    A4.place(x=300, y=255)
    A4.create_line(0, 10, 50, 10, arrow="last", width=3, arrowshape=(10, 12, 5))
    A4 = Canvas(robot_GUI, highlightthickness=0)
    A4.place(x=230, y=285)
    A4.create_line(10, 0, 10, 30, arrow="last", width=3, arrowshape=(10, 12, 5))
    B2_TAREFA_1 = Button(robot_GUI,
                         text ="DE NOVO",
                         command = lambda: fala(1059, 1356, 843, 1851, "", 7, 2,11)).place(x=200, y=320)
                                 
    B3_TAREFA_2 = Button(robot_GUI,
                         text ="OBJETO 2",
                         command = lambda: fala(1149, 1446, 1203, 1851, "", 7, 2,10)).place(x=365, y=250)
    A5 = Canvas(robot_GUI, highlightthickness=0)
    A5.place(x=465, y=255)
    A5.create_line(0, 10, 50, 10, arrow="last", width=3, arrowshape=(10, 12, 5))
    A5 = Canvas(robot_GUI, highlightthickness=0)
    A5.place(x=400, y=285)
    A5.create_line(10, 0, 10, 30, arrow="last", width=3, arrowshape=(10, 12, 5))
    B3_TAREFA_1 = Button(robot_GUI,
                         text ="DE NOVO",
                         command = lambda: fala(1149, 1446, 1203, 1851, "",7, 2,10)).place(x=370, y=320)
                         
    B4_TAREFA_2 = Button(robot_GUI,
                         text ="OBJETO 3",
                         command = lambda: fala(1660, 1302, 1460, 2040, "",7, 4,8)).place(x=530, y=250)
    A6 = Canvas(robot_GUI, highlightthickness=0)
    A6.place(x=565, y=285)
    A6.create_line(10, 0, 10, 30, arrow="last", width=3, arrowshape=(10, 12, 5))
    B3_TAREFA_1 = Button(robot_GUI,
                         text ="DE NOVO",
                         command = lambda: fala(1660, 1302, 1460, 2040, "", 7, 4,8)).place(x=530, y=320)
                              
    f=Frame(robot_GUI, height=2 , width=640, bg="black")
    f.place(x=0, y=360)
    ################################################################################################
    Label(robot_GUI, text = "TAREFA 3 (OLHAR + APONTAR + FALAR)").place(x=190, y=370)

    B1_TAREFA_3 = Button(robot_GUI,
                         text ="INTRODUCAO", 
                         command = lambda: fala(1824, 1851, 1860, 1500,"outra_vez.wav")).place(x=20, y=405)                            
    A = Canvas(robot_GUI, highlightthickness=0)
    A.place(x=140, y=410)
    A.create_line(0, 10, 50, 10, arrow="last", width=3, arrowshape=(10, 12, 5)) 
    
    B2_TAREFA_3 = Button(robot_GUI,
                         text ="OBJETO 1",
                         command = lambda: fala(1059, 1356, 843, 1851, "Helicoptero.wav",7,2,11)).place(x=200, y=405)
    A4 = Canvas(robot_GUI, highlightthickness=0)
    A4.place(x=300, y=410)
    A4.create_line(0, 10, 50, 10, arrow="last", width=3, arrowshape=(10, 12, 5))
    A4 = Canvas(robot_GUI, highlightthickness=0)
    A4.place(x=230, y=440)
    A4.create_line(10, 0, 10, 30, arrow="last", width=3, arrowshape=(10, 12, 5))
    B2_TAREFA_1 = Button(robot_GUI,
                         text ="DE NOVO",
                         command = lambda: fala(1059, 1356, 843, 1851, "Helicoptero.wav",7,2,11)).place(x=200, y=475)
                              
    B3_TAREFA_3 = Button(robot_GUI,
                         text ="OBJETO 2",
                         command = lambda: fala(1149, 1446, 1203, 1851, "Caminhao.wav",0,2,10)).place(x=365, y=405)
    A5 = Canvas(robot_GUI, highlightthickness=0)
    A5.place(x=465, y=410)
    A5.create_line(0, 10, 50, 10, arrow="last", width=3, arrowshape=(10, 12, 5))
    A5 = Canvas(robot_GUI, highlightthickness=0)
    A5.place(x=400, y=440)
    A5.create_line(10, 0, 10, 30, arrow="last", width=3, arrowshape=(10, 12, 5))
    B3_TAREFA_1 = Button(robot_GUI,
                         text ="DE NOVO",
                         command = lambda: fala(1149, 1446, 1203, 1851, "Caminhao.wav",7,2,10)).place(x=370, y=475)

    B4_TAREFA_3 = Button(robot_GUI,
                         text ="OBJETO 3",
                         command = lambda: fala(1660, 1302, 1460, 2040, "Trem.wav",0,4,8)).place(x=530, y=405)
    A6 = Canvas(robot_GUI, highlightthickness=0)
    A6.place(x=565, y=440)
    A6.create_line(10, 0, 10, 30, arrow="last", width=3, arrowshape=(10, 12, 5))
    B3_TAREFA_1 = Button(robot_GUI,
                         text ="DE NOVO",
                         command = lambda: fala(1660, 1302, 1460, 2040, "Trem.wav",7,4,8)).place(x=530, y=475)

    f=Frame(robot_GUI, height=2 , width=640, bg="black")
    f.place(x=0, y=510)
    
    ################################################################################################ 
    Label(robot_GUI, text = "AUDIOS DO BEM").place(x=70, y=520)    
    B_SOM_1 = Button(robot_GUI,
                     text ="PARABENS",
                     command = lambda: som("Parabens.wav")).place(x=20, y=550)
    B_SOM_2 = Button(robot_GUI,
                     text ="MUITO BEM",
                     command = lambda: som("Muito_Bem.wav")).place(x=130, y=550)                
    
    Label(robot_GUI, text = "DESPEDIDA").place(x=290, y=520) 
    B_SOM_2 = Button(robot_GUI,
                     text ="TCHAU",
                     command = lambda: som("tchau.wav")).place(x=295, y=550)
                                                                         
    Label(robot_GUI, text = "DESCANSAR").place(x=500, y=520)    
    B_DESCANSO_1 = Button(robot_GUI,
                          text ="BRACO_OLHO",
                          command = lambda: fala(1460, 1600, 1555, 1660, "", 0, 2, 8)).place(x=495, y=550)
                  
    B_FELIZ = Button(robot_GUI,
                     text ="FELIZ",
                     command = lambda: emotion(18.5)).place(x=190, y=625)
    B_NEUTRO = Button(robot_GUI,
                      text ="NEUTRO",
                      command = lambda: emotion(0)).place(x=290, y=625)                              
    B_TRISTE = Button(robot_GUI,
                      text ="TRISTE",
                      command = lambda: emotion(198)).place(x=390, y=625)  
                                                                                                                             
    robot_GUI.mainloop()

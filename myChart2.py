# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 18:23:19 2017

@author: Yaolinjun
"""
from pylab import mpl                #导入pylab用于设置默认字体，matplotlib默认不支持中文显示
import matplotlib.pyplot as plt      #导入matplotlib用于绘图
import struct                        #导入struct用于二进制解析
from tkinter.filedialog import *
from tkinter import *                #导入tkinter用于图ffgfgg形界面绘制
import numpy as np

def InitUI():
     global fileName                                     #声明打开的文件
     global textBox                                      #声明消息栏UI
     global inputBox                                     #声明输入栏UI
     
     initSampleInterval=Variable()                       #声明初始的输入栏中的采样间距值
     initSampleInterval.set("1")                         #将间距值设置为1
     
     root.title('显示任意波形的Chart系统')
     
     textBox = Text(root, width='50', height='15')   
     
     textBox.insert('1.0', "                 ***使用说明***\n")
     
     textBox.insert('2.0', "          请通过选择文件进行波形的绘制\n")
     
     textBox.pack(fill=X)
     
     inputBoxLabel=Label(root, text="绘图采样点间隔")  
     
     inputBoxLabel.pack(side=LEFT)
     
     
     inputBox = Entry(root,textvariable=initSampleInterval,background = 'yellow')  #正确
     inputBox.pack(side=LEFT)
    
     
     #InputBox.contents = StringVar()
     button = Button(root, text="请选择目标文件", command=GetFileAndDraw)
         
     button.pack(fill=X)
     
     
def GetFileAndDraw():
    
    MAX_DRAW_COUNT=10000                          #确定绘制最大绘制的点数
    
    #stride=1                                     #采样点的间隔默认为1
    
    yAxisTuple=()
    
    xAxisList=[]
    
    ix = 1 
    
    fileName = filedialog.askopenfilename(filetypes=[("所有文件", "*")])
    
    textBox.insert('3.0',"\t当前打开的文件名："+fileName+"\n")
    
    file = open(fileName, 'rb')                    # 以二进制的方式打开对应的文件
    
    file.seek(0,2)                                   # 移动到文件内容的尾部
    
    fileLength=file.tell()                            #求出文件的长度
    
    file.seek(0,0)                            #回到文件内容的首部
    
    inputSampleInterval=int(inputBox.get())                        #将输入框输入的值设置转为Int型

    stride=inputSampleInterval
    
    print(stride)
    if(fileLength/stride)>MAX_DRAW_COUNT:                        #如果文件过长超过最大绘制点数
        fileLength=MAX_DRAW_COUNT                       
    while file.tell()<fileLength:
        yAxisTuple += struct.unpack('h', file.read(2)) 
        file.seek(stride, 1)                             #将文件指针向后移动stride单位长度
        xAxisList.append(ix)        
        ix=ix+1
        
    yAxisList = list(yAxisTuple)
    
    (outputxAxisList,outputyAxisList)=MyTrapZ(xAxisList,yAxisList)
    
    DrawChart(xAxisList,yAxisList,outputxAxisList,outputyAxisList,fileName)
    
    #drawMyTrapZ(xAxisList,yAxisList)      
    #y=np.trapz(yAxisList[1:5],xAxisList[1:5])
    #print(y)
def MyTrapZ(xAxisList,yAxisList):                 #梯形法求积分并绘制
    outputxAxisList=[]
    outputyAxisList=[]
    ix=0
    for i in range(len(xAxisList)):
        if(i%10==0 and i!=0):
            youtPut=np.trapz(yAxisList[i-10:i],xAxisList[i-10:i])
            outputyAxisList.append(youtPut)
            ix=ix+1
            outputxAxisList.append(ix)
    return(outputxAxisList,outputyAxisList)
    
def DrawChart(xAxisList,yAxisList,outputxAxisList,outputyAxisList,fileName):
    plt.figure(12)
    plt.subplot(2,1,1)
    plt.plot(xAxisList,yAxisList,'b')
    plt.title('绘制的图为'+fileName)
    plt.xlabel('x轴:坐标点')   
    plt.ylabel('y轴:对应的数据值')   
    plt.subplot(2,1,2)
    plt.plot(outputxAxisList,outputyAxisList,'m')
    plt.ylabel('y轴:积分后的值')   
    plt.xlabel('x轴:每隔10个坐标点进行一次积分后x的坐标点') 
    plt.show()
    
    
    
    
    
mpl.rcParams['font.sans-serif'] = ['FangSong']      # 字体设置为雅黑

mpl.rcParams['axes.unicode_minus'] = False          # 解决负号'-'显示为


root=Tk()

InitUI()                                            #显示初始界面

mainloop()

#drawChart(GetFileName)





    
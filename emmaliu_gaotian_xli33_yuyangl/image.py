#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 22:21:50 2019

@author: mac
"""
import matplotlib.pyplot as plt 

def loadTweets():
     with open("/Users/mac/Desktop/tweets_amman.json", 'r') as f:
         temp=json.loads(f.read())
         #length=len(temp)
         place=[]
         bounding=[]
         location=[]
         position=[]
         #print(length)
         for i in range(0,len(temp)):
             if temp[i]['place']!=None:
                 place.append(temp[i]['place'])
         for j in range(0,len(place)):
             if place[j]['bounding_box']!=None:
                 bounding.append(place[j]['bounding_box'])
         for k in range(0,len(bounding)):
             if bounding[k]['coordinates']!=None:
                 location.append(bounding[k]['coordinates'])
                 
#         print(len(location[0][0]))
                 
         for m in range (0,len(location)):
             for n in range (0,len(location[m][0])):
                 #if location[m][0][n] not in position:
                 position.append(location[m][0][n])
                     
         print(len(position))
         return position
     

t=loadTweets();
x=[]
y=[]
for i in range (0,len(t)):
   x.append(t[i][0])
   y.append(t[i][1])
#print(len(x))
#print(len(y))
   
plt.xlim(xmax=39,xmin=32)
plt.ylim(ymax=35,ymin=30)
plt.scatter(x,y)
plt.show()

    
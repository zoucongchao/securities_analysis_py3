# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 10:28:46 2018

@author: Administrator
"""



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter,WeekdayLocator, \
DayLocator,MONDAY,date2num
from matplotlib.finance import candlestick_ohlc

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def draw_Kline1(code,num=22):
    
    hist = pd.read_csv('C:/Users/Administrator/stockPriditionProjects/data/'+code+'.csv')
    hist.index = hist.iloc[:,0]
    hist=hist.iloc[::-1]
    hist.index = pd.to_datetime(hist.index,format='%Y-%m-%d')
    hist = hist.iloc[:,1:]
    #candleplot(hist)
    
    for i in range(len(hist)-num):
        print("step"+str(i)+"*"*20)
        seriesdata = hist.iloc[i:i+22]
    
        Date = [date2num(date) for date in seriesdata.index]
        seriesdata.loc[:,'Date'] = Date
               
        listData = []
        for j in range(len(seriesdata)):
            a= [seriesdata.Date[j], \
                seriesdata.open[j],seriesdata.high[j], \
                seriesdata.low[j],seriesdata.close[j]]
            listData.append(a)
            
       
        ax = plt.subplot()
        
        
        
        ax.xaxis_date()
        plt.xticks(rotation=45)
        '''
        mondays = WeekdayLocator(MONDAY)
        weekformatter = DateFormatter('%y %b %d')
        ax.xaxis.set_major_formatter(weekformatter)
        
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_major_locator(DayLocator())
        
        '''    
        candlestick_ohlc(ax,listData,width=0.5, \
                          colorup ='r',colordown='g')
        
        #ax.set_title(title)
        plt.savefig('D:/hellodata/candleplot/601336_'+str(i)+'.jpg')
    
    return(plt.show())

candleplot('601336')

def draw_Kline2(code,num=22):
    
    hist = pd.read_csv('C:/Users/Administrator/stockPriditionProjects/data/'+code+'.csv')
    hist.index = hist.iloc[:,0]
    hist=hist.iloc[::-1]
    hist.index = pd.to_datetime(hist.index,format='%Y-%m-%d')
    hist = hist.iloc[:,1:]
    #candleplot(hist)
    
    for i in range(len(hist)-num):
        print("step"+str(i)+"*"*20)
        seriesdata = hist.iloc[i:i+22]
    
        Date = [date2num(date) for date in seriesdata.index]
        seriesdata.loc[:,'Date'] = Date
               
        listData = []
        for j in range(len(seriesdata)):
            a= [seriesdata.Date[j], \
                seriesdata.open[j],seriesdata.high[j], \
                seriesdata.low[j],seriesdata.close[j]]
            listData.append(a)
            
       
        ax = plt.subplot()
        
        
        
        ax.xaxis_date()
        plt.xticks(rotation=45)
        '''
        mondays = WeekdayLocator(MONDAY)
        weekformatter = DateFormatter('%y %b %d')
        ax.xaxis.set_major_formatter(weekformatter)
        
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_major_locator(DayLocator())
        
        '''    
        candlestick_ohlc(ax,listData,width=0.5, \
                          colorup ='r',colordown='g')
        
        #ax.set_title(title)
        plt.savefig('D:/hellodata/candleplot/601336_'+str(i)+'.jpg')
    
    return(plt.show())
"""
hist = pd.read_csv('C:/Users/Administrator/stockPriditionProjects/data/601336.csv')
hist.index = hist.iloc[:,0]
hist=hist.iloc[::-1]
hist.index = pd.to_datetime(hist.index,format='%Y-%m-%d')
hist = hist.iloc[:,1:]
#candleplot(hist)
num = 22
for i in range(len(hist)-num):
    hist = hist.iloc[i:i+22]
    candleplot(hist)
"""    
#hist = hist.iloc[720:]
#candleplot(hist)





#candleplot(histdata,title='上证指数日K线图')


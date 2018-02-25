# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 06:50:13 2018

@author: Administrator
"""

import pandas as pd
import csv
from sklearn import preprocessing
import numpy as np
from data_preprocess import load_data
from data_preprocess import Extract_Features

#bin() 返回一个整数 int 或者长整数 long int 的二进制表示。
def covert_bin(x, covert_len):
    x = str(bin(x))[2:]
    print(x)
    if (len(x)<covert_len):
        x = ''.join('0' for _ in range(covert_len - len(x))) + x

    x = [int(c) for c in x]
    return x

#开盘价**********************************************************************************************
def get_open_price(code, date):
    '''
    获取开盘价
    :param code:股票代码
    :param date: 日期
    :return:
    '''
    data = pd.read_csv('C:/Users/Administrator/stockPriditionProjects/data/' + str(code) + '.csv', index_col='date')
    open_price = data['open']
    return open_price[date]

#盘中价**********************************************************************************************
def get_am_pm_price(code, date):
    '''
    :param code: 股票代码
    :param date: 股票查询日期
    :return: 该股票在该日期下对应的早上约10点,下午约2:30的价格
    '''
    if type(code) is not str or type(date) is not str:
        code = str(code)
        date = str(date)
    import tushare as ts
    df = ts.get_tick_data(code, date)
    dtime = df.set_index('time')
    price = dtime['price']
    if price.shape == (0,):
        print(code, "can't get ", date, "am_pm data!")
        return float('nan'), float('nan')
    else:
        return price[-1], price[int(len(df.time)/4)]
    
#开盘价和收盘价**********************************************************************************************
def get_open_close_hist_price(code, start_date=None, end_date=None):
    '''
    :param code: 股票代码
    :param date: 股票查询日期
    :return: 该股票在该open close 的价格
    '''
    import tushare as ts
    if start_date != None and end_date != None:

        if type(code) is not str or type(start_date) is not str:
            code = str(code)
            start_date = str(start_date)
            end_date = str(end_date)

        df = ts.get_hist_data(code, start_date,end_date)
        openPrice = df['open'][0]
        closePrice = df['close'][0]
        return openPrice,closePrice
        '''
        dtime = df.set_index('time')
        price = dtime['price']
        if price.shape == (0,):
            print(code, "can't get ", start_date, "am_pm data!")
            return float('nan'), float('nan')
        else:
            return price[-1], price[int(len(df.time)/4)]
        '''

    else:
        df = ts.get_hist_data(code)
        openPrice = df['open'][0]
        closePrice = df['close'][0]
        return openPrice,closePrice
        '''
        dtime = df.set_index('time')
        price = dtime['price']
        if price.shape == (0,):
            print(code, "can't get ", start_date, "am_pm data!")
            return float('nan'), float('nan')
        else:
            return price[-1], price[int(len(df.time)/4)]
        '''

#交叉验证**************************************************************************************
def read_sort_result(sort_results_path):
    '''
    交叉验证结果保存在./data/cvmodel/sort_results_600.csv
    近XX天作测试结果保存在./data/sort_results_600.csv
    :return: 读取排序结果
    '''
    #data_file = open('../data/cvmodel/sort_results_600.csv', 'r')
    data_file = open(sort_results_path, 'r')  #'./data/sort_results_sz.csv'
    data_reader = csv.reader(data_file)
    sort = []
    for row in data_reader:
        sort.append(row)
    return sort

#MLP训练数据**************************************************************************************
def get_data_for_MLP(code):
    '''
    :param code: 股票代码
    :return: MLP训练数据X, y
    '''
    data_path = 'C:/Users/Administrator/stockPriditionProjects/data/'
    oneDayLine, date = load_data.load_data_from_tushare(data_path + str(code) + '.csv')
    volumn, volumn_dates = load_data.load_volume_from_tushare(data_path + str(code) + '.csv')
    daynum = 5
    X = []
    y = []
    ef = Extract_Features.Extract_Features()
    for i in range(daynum, len(date)):
        X_delta = [oneDayLine[k] - oneDayLine[k - 1] for k in range(i - daynum, i)] + \
                  [volumn[k] for k in range(i - daynum, i)] + \
                  [float(ef.parse_weekday(date[i - 1]))] + \
                  [float(ef.lunar_month(date[i - 1]))] + \
                  [ef.rrr(date[i - 1])] + \
                  [ef.MoneySupply(date[i - 1])]
        X.append(X_delta)
        y.append([1, 0] if oneDayLine[i] - oneDayLine[i - 1] >= 0 else [0, 1])
    return np.array(X), np.array(y)

#MLP预测数据**************************************************************************************
def get_today_data_for_MLP(code):
    '''
    :param code:股票代码
    :return: 今日预测的X
    '''
    import numpy as np
    data_path = 'C:/Users/Administrator/stockPriditionProjects/data/'
    oneDayLine, date = load_data.load_data_from_tushare(data_path + str(code) + '.csv')
    volumn, volumn_dates = load_data.load_volume_from_tushare(data_path + str(code) + '.csv')
    daynum = 5
    X = []
    ef = Extract_Features.Extract_Features()
    for i in range(daynum, len(date)):
        X_delta = [oneDayLine[k] - oneDayLine[k - 1] for k in range(i - daynum, i)] + \
                  [volumn[k] for k in range(i - daynum, i)] + \
                  [float(ef.parse_weekday(date[i]))] + \
                  [float(ef.lunar_month(date[i]))] + \
                  [ef.rrr(date[i])] + \
                  [ef.MoneySupply(date[i])]
        X.append(X_delta)

    X = preprocessing.MinMaxScaler().fit_transform(X)
    return np.array(X[-1])

def get_today_more_data_for_MLP(code):
    '''
    :param code:股票代码
    :return: 今日预测的X
    '''
    stock_data_path = 'C:/Users/Administrator/stockPriditionProjects/data/'
    open_price, oneDayLine, volume, ma5, vma5, turnover, dates = load_data.load_fq_open_close_volume_ma5_vma5_turnover_from_tushare(
        stock_data_path + str(code) + '_fq.csv')


    if (str(code)[0] == '6'):
        # 上证指数
        open_index, close_index, volume_index, ma5_index, vma5_index, dates_index = load_data.load_index_open_close_volume_ma5_vma5_from_tushare(
            stock_data_path + 'sh.csv')
    else:
        # 深证指数
        open_index, close_index, volume_index, ma5_index, vma5_index, dates_index = load_data.load_index_open_close_volume_ma5_vma5_from_tushare(
            stock_data_path + 'sz.csv')
    daynum = 5
    X_clf = []
    ef = Extract_Features.Extract_Features()


    for i in range(daynum, len(dates)):
        #以大盘为标准
        p = dates_index.index(dates[i])
        # 组装数据
        X_delta = [(oneDayLine[k] - oneDayLine[k - 1]) / oneDayLine[k - 1] for k in range(i - daynum, i)] + \
                  [(volume[k] - volume[k - 1]) / volume[k - 1] for k in range(i - daynum, i)] + \
                  [turnover[k] for k in range(i - daynum, i)] + \
                  [(ma5[i] - ma5[i - 1]) / ma5[i - 1]] + \
                  [(vma5[i] - vma5[i - 1]) / vma5[i - 1]] + \
                  [(open_index[p] - open_index[p - 1]) / open_index[p - 1]] + \
                  [(close_index[p] - close_index[p - 1]) / close_index[p - 1]] + \
                  [(volume_index[p] - volume_index[p - 1]) / volume_index[p - 1]] + \
                  [(ma5_index[p] - ma5_index[p - 1]) / ma5_index[p - 1]] + \
                  [(vma5_index[p] - vma5_index[p - 1]) / vma5_index[p - 1]] + \
                  covert_bin(ef.parse_weekday(dates[i]), 3) \
                  # + [(ef.MoneySupply(dates[i]) - ef.MoneySupply(dates[i - 22])) / ef.MoneySupply(dates[i - 22])]
        # covert_bin(ef.lunar_month(dates[i]), 5) + \
        if i == 5:
            X_delta[0] = X_delta[5] = 0.0  # 调整第一个百分比
        X_clf.append(X_delta)
    X_clf = preprocessing.MinMaxScaler().fit_transform(X_clf)
    # return np.array(X_clf)
    return X_clf[-1]

#最近一个月的MLP测试数据***************************************************************************************************************
def get_last_month_data_for_MLP(code):
    '''
    :param code:股票代码
    :return: MLP最近一个月(修改参数在函数内的num)的MLP测试数据
    '''
    stock_data_path = 'C:/Users/Administrator/stockPriditionProjects/data/'
    oneDayLine, date = load_data.load_data_from_tushare(stock_data_path + str(code) + '.csv')
    volumn, volumn_dates = load_data.load_volume_from_tushare(stock_data_path + str(code) + '.csv')
    # each data consist of delta od last daynum days
    daynum = 5
    num = 22
    X_clf = []
    y_clf = []
    ef = Extract_Features.Extract_Features()
    for i in range(len(date)-num-daynum, len(date)):
        X_delta = [oneDayLine[k] - oneDayLine[k - 1] for k in range(i - daynum, i)] + \
                  [volumn[k] for k in range(i - daynum, i)] + \
                  [float(ef.parse_weekday(date[i - 1]))] + \
                  [float(ef.lunar_month(date[i - 1]))] + \
                  [float(ef.rrr(date[i - 1]))] + \
                  [float(ef.MoneySupply(date[i - 1]))]
        X_clf.append(X_delta)
        y_clf.append([1, 0] if oneDayLine[i] - oneDayLine[i - 1] >= 0 else [0, 1])
    return np.array(X_clf), np.array(y_clf)

def get_last_month_more_data_for_MLP(code):
    '''
    :param code:股票代码
    :return: MLP最近一个月(修改参数在函数内的num)的MLP测试数据
    '''
    stock_data_path = 'C:/Users/Administrator/stockPriditionProjects/data/'

    open_price, oneDayLine, volume, ma5, vma5, turnover, dates = load_data.load_fq_open_close_volume_ma5_vma5_turnover_from_tushare(
        stock_data_path + str(code) + '_fq.csv')

    if (str(code)[0] == '6'):
        # 上证指数
        open_index, close_index, volume_index, ma5_index, vma5_index, dates_index = load_data.load_index_open_close_volume_ma5_vma5_from_tushare(
            stock_data_path + 'sh.csv')
    else:
        # 深证指数
        open_index, close_index, volume_index, ma5_index, vma5_index, dates_index = load_data.load_index_open_close_volume_ma5_vma5_from_tushare(
            stock_data_path + 'sz.csv')

    daynum = 5
    num = 22
    X_clf = []
    ef = Extract_Features.Extract_Features()
    
    for i in range(daynum, len(dates)):
        #以大盘为标准
        p = dates_index.index(dates[i])
        # 组装数据
        X_delta = [(oneDayLine[k] - oneDayLine[k - 1]) / oneDayLine[k - 1] for k in range(i - daynum, i)] + \
                  [(volume[k] - volume[k - 1]) / volume[k - 1] for k in range(i - daynum, i)] + \
                  [turnover[k] for k in range(i - daynum, i)] + \
                  [(ma5[i] - ma5[i - 1]) / ma5[i - 1]] + \
                  [(vma5[i] - vma5[i - 1]) / vma5[i - 1]] + \
                  [(open_index[p] - open_index[p - 1]) / open_index[p - 1]] + \
                  [(close_index[p] - close_index[p - 1]) / close_index[p - 1]] + \
                  [(volume_index[p] - volume_index[p - 1]) / volume_index[p - 1]] + \
                  [(ma5_index[p] - ma5_index[p - 1]) / ma5_index[p - 1]] + \
                  [(vma5_index[p] - vma5_index[p - 1]) / vma5_index[p - 1]] + \
                  covert_bin(ef.parse_weekday(dates[i]), 3) \
                  # + [(ef.MoneySupply(dates[i]) - ef.MoneySupply(dates[i - 22])) / ef.MoneySupply(dates[i - 22])]
        # covert_bin(ef.lunar_month(dates[i]), 5) + \
        if i == 5:
            X_delta[0] = X_delta[5] = 0.0  # 调整第一个百分比
        X_clf.append(X_delta)
    X_clf = preprocessing.MinMaxScaler().fit_transform(X_clf)
    # return np.array(X_clf)
    return X_clf

#最近N天的MLP测试数据***************************************************************************************************************
def get_last_N_days_data_for_MLP(code, N):
    '''
    :param code:股票代码
    :return: MLP最近N天(修改参数在函数内的num)的MLP测试数据
    '''
    data_path = 'C:/Users/Administrator/stockPriditionProjects/data/'
    oneDayLine, date = load_data.load_data_from_tushare(data_path + str(code) + '.csv')
    volumn, volumn_dates = load_data.load_volume_from_tushare(data_path + str(code) + '.csv')
    # each data consist of delta od last daynum days
    daynum = 5
    num = N
    X_clf = []
    y_clf = []
    ef = Extract_Features.Extract_Features()
    for i in range(len(date)-num, len(date)):
        X_delta = [oneDayLine[k] - oneDayLine[k - 1] for k in range(i - daynum, i)] + \
                  [volumn[k] for k in range(i - daynum, i)] + \
                  [float(ef.parse_weekday(date[i - 1]))] + \
                  [float(ef.lunar_month(date[i - 1]))] + \
                  [float(ef.rrr(date[i - 1]))] + \
                  [float(ef.MoneySupply(date[i - 1]))]
        X_clf.append(X_delta)
        y_clf.append([1, 0] if oneDayLine[i] - oneDayLine[i - 1] >= 0 else [0, 1])
    return np.array(X_clf), np.array(y_clf)

#读取相关信息**************************************************************************************************************************
def read_stock_dict():
    '''
    读取存储的持有股票信息
    :return:
    '''
    data_file = open('./data/cvmodel/stock_dict.csv', 'r')
    data_reader = csv.reader(data_file)
    stock_dict = {}
    for row in data_reader:
        stock_dict[row[0]] = row[1]
    return stock_dict

def get_today_open_price(code):
    '''
    :param code:股票代码
    :return:今日开盘价
    '''
    import tushare as ts
    return ts.get_realtime_quotes(code)['open']

def get_today_close_price(code):
    '''
    :param code:股票代码
    :return: 今日收盘价
    '''
    import tushare as ts
    return ts.get_realtime_quotes(code)['close']
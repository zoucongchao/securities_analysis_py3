# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 07:19:47 2018

@author: Administrator
"""

import numpy as np
from sklearn import preprocessing
import os
import numpy


def download_from_tushare(code):
    '''
    #宏观经济形势,数字指标1:货币供应量
    month :统计时间
    m2 :货币和准货币（广义货币M2）(亿元)
    m2_yoy:货币和准货币（广义货币M2）同比增长(%)
    m1:货币(狭义货币M1)(亿元)
    m1_yoy:货币(狭义货币M1)同比增长(%)
    m0:流通中现金(M0)(亿元)
    m0_yoy:流通中现金(M0)同比增长(%)
    cd:活期存款(亿元)
    cd_yoy:活期存款同比增长(%)
    qm:准货币(亿元)
    qm_yoy:准货币同比增长(%)
    ftd:定期存款(亿元)
    ftd_yoy:定期存款同比增长(%)
    sd:储蓄存款(亿元)
    sd_yoy:储蓄存款同比增长(%)
    rests:其他存款(亿元)
    rests_yoy:其他存款同比增长(%)
    '''
    import tushare as ts
    path = 'C:/Users/Administrator/stockPriditionProjects/data/'

    # 1 day line
    hist_data = ts.get_hist_data(str(code))
    if hist_data is not None:
        hist_data.to_csv(path+str(code)+'.csv')
        return True
    else:
        return False
    # 30 day lines
    # ts.get_hist_data(str(code), ktype='M').to_csv(path+"stock_data/"+str(code)+'_month.csv')

def download_fq_data_from_tushare(code):
    '''
    必须下载历史数据，根据历史数据日期请求复盘数据，这里是前复盘
    :param code:
    :return:
    '''
    path = 'C:/Users/Administrator/stockPriditionProjects/data/'
    import tushare as ts
    import datetime
    sh_index_lastday = open(path+'000001.csv', 'rb').readlines()[1:][0]  # 取上证最后一天日期做比对，如果个股没有则不存储
    sh_index_lastday = sh_index_lastday.decode('utf-8')
    # if os.path.exists(path+'stock_data/' + str(code) + '.csv'):
    #     import tushare as ts
    #
    #     f = open(path+'stock_data/' + str(code) + '.csv', 'rb').readlines()[1:]
    #     # 3years line
    #     fp_data = ts.get_h_data(str(code), start=f[-1].split(',')[0], end=f[0].split(',')[0])
    #     if fp_data is not None:
    #         fp_data.to_csv(path+"stock_data/"+str(code)+'_fq.csv')
    #         # ts.get_h_data(str(code), start=raw_dates[0], end=raw_dates[-1]).to_csv(path+"stock_data/"+str(code)+'_fq.csv')
    #         return True
    #     else:
    #         return False
    # else:
    #     return False
    years = 3
    start = datetime.datetime.today().date() + datetime.timedelta(-365 * years)
    # 3years line
    # fp_data = ts.get_h_data(str(code), start=str(start))
    fp_data = ts.get_k_data(str(code), start=str(start))
    if fp_data is not None and len(fp_data) > 1 and fp_data['date'].tolist()[-1] == sh_index_lastday.split(',')[0]:
        fp_data.to_csv(path + str(code) + '_fq.csv')
        return True
    else:
        return False
    
def download_economy():
    import tushare as ts
    path = 'C:/Users/Administrator/stockPriditionProjects/data/'
    ts.get_money_supply().to_csv(path+'money_supply.csv')
    ts.get_gdp_quarter().to_csv(path+'gdp_quarter.csv')
    ts.get_gdp_year().to_csv(path + 'gdp_year.csv')
    ts.get_cpi().to_csv(path+'cpi.csv')
    # ts.get_hist_data('sz').to_csv(path + 'sz.csv')
    # ts.get_hist_data('sh').to_csv(path + 'sh.csv')

    # import time
    import datetime
    # now_year = time.localtime().tm_year
    # now_mon = time.localtime().tm_mon
    # now_day = time.localtime().tm_mday
    years = 3
    start = datetime.datetime.today().date() + datetime.timedelta(-365*years)
    end = datetime.datetime.today().date()
    ts.get_k_data('399001',  start=str(start), index=True).to_csv(path + 'sz.csv')  #默认2年 ,
    ts.get_k_data('000001',  start=str(start), index=True).to_csv(path + 'sh.csv')
    #存款准备金率
    ts.get_rrr().to_csv(path + 'rrr.csv')
    

def load_data(path):
    '''
    load data from quandl
    :return:close_price,dates
    '''
    f = open(path, 'rb').readlines()[1:]
    raw_close_data = []
    raw_open_data = []
    raw_dates = []
    for line in f:
        line = line.decode('utf-8')
        try:
            close_price = float(line.split(',')[3])
            raw_close_data.append(close_price)

            open_price = float(line.split(',')[1])
            raw_open_data.append(open_price)

            raw_dates.append(line.split(',')[0])
        except:
            continue
    return raw_open_data, raw_close_data, raw_dates     #inverse order

#开盘价
def load_open_price(path):
    '''
    load data from quandl
    :return:open_price,dates
    '''
    f = open(path, 'rb').readlines()[1:]
    raw_data = []
    raw_dates = []
    for line in f:
        line = line.decode('utf-8')
        try:
            open_price = float(line.split(',')[1])
            raw_data.append(open_price)
            raw_dates.append(line.split(',')[0])
        except:
            continue
    return raw_data[::-1], raw_dates[::-1]     #inverse order

#收盘价
def load_data_from_tushare(path):
    '''
    load data from tushare
    :return:close_price,dates
    '''
    f = open(path, 'rb').readlines()[1:]
    raw_data = []
    raw_dates = []
    for line in f:
        line = line.decode('utf-8')
        try:
            close_price = float(line.split(',')[3])
            raw_data.append(close_price)
            raw_dates.append(line.split(',')[0])
        except:
            continue
    return raw_data[::-1], raw_dates[::-1]  # inverse order

def load_open_close_volume_ma5_vma5_turnover_from_tushare(path):
    '''
    load data from tushare
    :return:ma5,vma5,dates
    '''
    f = open(path, 'rb').readlines()[1:]
    raw_open_price = []
    raw_close_price = []
    raw_volume = []
    raw_ma5 = []
    raw_vma5 = []
    raw_turnover = []
    raw_dates = []
    for line in f:
        line = line.decode('utf-8')
        try:
            open_price = float(line.split(',')[1])
            raw_open_price.append(open_price)

            close_price = float(line.split(',')[3])
            raw_close_price.append(close_price)

            volume = float(line.split(',')[5])
            raw_volume.append(volume)

            ma5 = float(line.split(',')[8])
            raw_ma5.append(ma5)

            vma5 = float(line.split(',')[11])
            raw_vma5.append(vma5)

            turnover = float(line.split(',')[14])
            raw_turnover.append(turnover)

            raw_dates.append(line.split(',')[0])
        except:
            continue
    return raw_open_price[::-1], raw_close_price[::-1], raw_volume[::-1], \
            raw_ma5[::-1], raw_vma5[::-1], raw_turnover[::-1], raw_dates[::-1]  # inverse order

def load_fq_open_close_volume_ma5_vma5_turnover_from_tushare(path):
    '''
    load fq data from tushare
    :return:ma5,vma5,dates
    '''
    fq_f = open(path, 'rb').readlines()[1:]
    #os.path.split 分离路径和文件名
    filepath = os.path.split(path)
    #os.path.splitext(path) 分离文件名与扩展名；默认返回(fname,fextension)元组
    prefix_filename = os.path.splitext(filepath[1])
    fn = prefix_filename[0].split('_')[0]

    f = open(os.path.join(filepath[0], fn)+'.csv', 'rb').readlines()[1:]
    fdates = [d.decode('utf-8').split(',')[0] for d in f]
    raw_open_price = []
    raw_close_price = []
    raw_volume = []
    raw_ma5 = []
    raw_vma5 = []
    raw_turnover = []
    raw_dates = []
    last_outstanding = 0.0
    for i, fq_line in enumerate(fq_f):
        fq_line = fq_line.decode('utf-8')
        try:

            open_price = float(fq_line.split(',')[2])
            raw_open_price.append(open_price)

            close_price = float(fq_line.split(',')[3])
            raw_close_price.append(close_price)

            volume = float(fq_line.split(',')[6])
            raw_volume.append(volume)

            if i < 5:
                line5_temp = fq_f[:i + 1]
            else:
                line5_temp = fq_f[i - 5 +1:i+1]

            ma5_temp = [float(m.decode('utf-8').split(',')[3]) for m in line5_temp]
            raw_ma5.append(numpy.mean(ma5_temp))

            vma5_temp = [float(m.decode('utf-8').split(',')[6]) for m in line5_temp]
            raw_vma5.append(numpy.mean(vma5_temp))

            if fq_line.split(',')[1] in fdates:
                date_index = fdates.index(fq_line.split(',')[1])
                line = f[date_index]
                line = line.decode('utf-8')
                turnover = float(line.split(',')[14])
            else:
                if last_outstanding == 0.0:
                    turnover = 0.6
                else:
                    turnover = volume / last_outstanding


            raw_turnover.append(turnover)
            if turnover == 0.0:
                turnover = 1
            last_outstanding = volume / turnover

            raw_dates.append(fq_line.split(',')[1])
        except Exception as e:
            print ('load_fq error : ',e)
            continue
    # return raw_open_price[::-1], raw_close_price[::-1], raw_volume[::-1], raw_ma5[::-1], raw_vma5[::-1], raw_dates[::-1] # inverse order
    return raw_open_price, raw_close_price, raw_volume, \
            raw_ma5, raw_vma5, raw_turnover, raw_dates
    # return raw_open_price[5:], raw_close_price[5:], raw_volume[5:], raw_ma5[5:], raw_vma5[5:], raw_dates[5:]

def load_fq_ma5_ma10_ma20_ma30_ma60_ma120_ma250_ma500_from_tushare(code):
    '''
    load fq data from tushare
    :return:ma5_ma10_ma20_ma30_ma60_ma120_ma250_ma500_,dates
    '''
    # if os.path.exists('./data/stock_data/'+str(code)+'.csv'):
    f = open('C:/Users/Administrator/stockPriditionProjects/data/'+str(code)+'.csv', 'rb').readlines()[1:]
    fdates = [d.decode('utf-8').split(',')[0] for d in f]
    fq_f = open('C:/Users/Administrator/stockPriditionProjects/data/'+str(code)+'_fq.csv', 'rb').readlines()[1:]
    raw_open_price = []
    raw_close_price = []
    raw_volume = []
    raw_ma5 = []
    raw_vma5 = []
    raw_turnover = []

    raw_ma10 = []
    raw_ma20 = []
    raw_ma30 = []
    raw_ma60 = []
    raw_ma120 = []
    raw_ma250 = []
    raw_ma500 = []
    raw_ma_order = []
    raw_dates = []
    for fq_line in fq_f:
        fq_line = fq_line.decode('utf-8')
        try:
            date_index = fdates.index(fq_line.split(',')[1])
            line = f[date_index]
            line = line.decode('utf-8')

            # open_price = float(line.split(',')[1])
            open_price = float(fq_line.split(',')[2])
            raw_open_price.append(open_price)

            # close_price = float(line.split(',')[3])
            close_price = float(fq_line.split(',')[3])
            raw_close_price.append(close_price)

            volume = float(fq_line.split(',')[6])
            raw_volume.append(volume)


            ma5_temp = fq_f[fq_f.index(fq_line):fq_f.index(fq_line)+5]
            ma5_temp = [float(m.split(',')[3]) for m in ma5_temp]
            # numpy.mean(ma5_temp)
            raw_ma5.append(numpy.mean(ma5_temp))

            ma10_temp = fq_f[fq_f.index(fq_line):fq_f.index(fq_line)+10]
            ma10_temp = [float(m.split(',')[3]) for m in ma10_temp]
            raw_ma10.append(numpy.mean(ma10_temp))

            ma20_temp = fq_f[fq_f.index(fq_line):fq_f.index(fq_line)+20]
            ma20_temp = [float(m.split(',')[3]) for m in ma20_temp]
            raw_ma20.append(numpy.mean(ma20_temp))

            ma30_temp = fq_f[fq_f.index(fq_line):fq_f.index(fq_line)+30]
            ma30_temp = [float(m.split(',')[3]) for m in ma30_temp]
            raw_ma30.append(numpy.mean(ma30_temp))

            ma60_temp = fq_f[fq_f.index(fq_line):fq_f.index(fq_line)+60]
            ma60_temp = [float(m.split(',')[3]) for m in ma60_temp]
            raw_ma60.append(numpy.mean(ma60_temp))

            ma120_temp = fq_f[fq_f.index(fq_line):fq_f.index(fq_line) + 120]
            ma120_temp = [float(m.split(',')[3]) for m in ma120_temp]
            raw_ma120.append(numpy.mean(ma120_temp))

            ma250_temp = fq_f[fq_f.index(fq_line):fq_f.index(fq_line) + 250]
            ma250_temp = [float(m.split(',')[3]) for m in ma250_temp]
            raw_ma250.append(numpy.mean(ma250_temp))

            ma500_temp = fq_f[fq_f.index(fq_line):fq_f.index(fq_line) + 500]
            ma500_temp = [float(m.split(',')[3]) for m in ma500_temp]
            raw_ma500.append(numpy.mean(ma500_temp))

            if numpy.mean(ma5_temp)<numpy.mean(ma10_temp)<numpy.mean(ma20_temp)<numpy.mean(ma30_temp)<numpy.mean(ma60_temp)<numpy.mean(ma120_temp)<numpy.mean(ma250_temp)<numpy.mean(ma500_temp):
                # print 'code',str(code),  fq_line.split(',')[0]
                raw_ma_order.append(1)
            else:
                raw_ma_order.append(0)

            # vma5 = float(line.split(',')[11])
            # raw_vma5.append(vma5)

            turnover = float(line.split(',')[14])
            raw_turnover.append(turnover)

            raw_dates.append(fq_line.split(',')[1])
        except:
            continue
    return raw_close_price[::-1], raw_ma5[::-1], raw_ma10[::-1], raw_ma20[::-1], \
            raw_ma30[::-1], raw_ma60[::-1], raw_ma120[::-1], raw_ma250[::-1], \
            raw_ma500[::-1], raw_ma_order[::-1], raw_turnover[::-1], raw_dates[::-1]  # inverse order
    # else:
    #     return

def load_index_open_close_volume_ma5_vma5_from_tushare(path):
    '''
    load index data from tushare
    :return:ma5,vma5,dates
    '''
    f = open(path, 'rb').readlines()[1:]
    # fq_f = open(path, 'rb').readlines()[1:]
    raw_open_price = []
    raw_close_price = []
    raw_volume = []
    raw_ma5 = []
    raw_vma5 = []
    raw_dates = []
    for i, line in enumerate(f):
        line = line.decode('utf-8')
        try:
            # index, date, open, close, high, low, volume, code
            open_price = float(line.split(',')[2])
            raw_open_price.append(open_price)

            close_price = float(line.split(',')[3])
            raw_close_price.append(close_price)

            volume = float(line.split(',')[6])
            raw_volume.append(volume)

            if i < 5:
                line5_temp = f[:i + 1]
            else:
                line5_temp = f[i - 5+1:i+1]

            ma5_temp = [float(m.decode('utf-8').split(',')[3]) for m in line5_temp]
            raw_ma5.append(numpy.mean(ma5_temp))

            vma5_temp = [float(m.decode('utf-8').split(',')[6]) for m in line5_temp]
            raw_vma5.append(numpy.mean(vma5_temp))


            raw_dates.append(line.split(',')[1])
        except:
            continue
    # return raw_open_price[::-1], raw_close_price[::-1], raw_volume[::-1], raw_ma5[::-1], raw_vma5[::-1], raw_dates[::-1]  # inverse order
    return raw_open_price, raw_close_price, raw_volume, raw_ma5, raw_vma5, raw_dates
    # return raw_open_price[5:], raw_close_price[5:], raw_volume[5:], raw_ma5[5:], raw_vma5[5:], raw_dates[5:]

















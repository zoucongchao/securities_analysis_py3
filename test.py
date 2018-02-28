# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 16:53:44 2018

@author: Administrator
"""

from data_preprocess import load_data
from data_preprocess import Extract_Features
path = 'C:/Users/Administrator/stockPriditionProjects/data/601336.csv'
code = '601336'

Open,close,date = load_data.load_data(path)
date = date[-1] 
print(date)

"""
Date = '2016-1-16'
daydate = Extract_Features.Extract_Features()
date0 = daydate.short_text_classification(date)
#print(date0)
"""

#aa,bb,cc,dd,ee,ff,gg,hh,ii,jj,kk,ll = load_data.load_index_open_close_volume_ma5_vma5_from_tushare(path)
#gg,hh,ii,jj,kk,ll = load_data.load_index_open_close_volume_ma5_vma5_from_tushare(path)
'''
gg,hh = load_data.To_DL_datatype(code)
print(gg[0],hh[0])
'''
#print(aa[-1],bb[-1],cc[-1],dd[-1],ee[-1],ff[-1],gg[-1],hh[-1],ii[-1],jj[-1],kk[-1],ll[-1]) 
"""
fq_f = open(path, 'rb').readlines()[1:]
#os.path.split 分离路径和文件名
filepath = os.path.split(path)
#os.path.splitext(path) 分离文件名与扩展名；默认返回(fname,fextension)元组
prefix_filename = os.path.splitext(filepath[1])
print(filepath[1])
fn = prefix_filename[0].split('_')[0]
print(prefix_filename[0])
print(filepath[0])
print(fn)

fh = os.path.join(filepath[0], fn)+'.csv'
print(fh)

for i, fq_line in enumerate(fq_f):
    fq_line = fq_line.decode('utf-8')
    if i==0:
        print(i,fq_line)
"""
"""
import datetime
from data_preprocess import lunar
def test(ct=None):
    ln = lunar.Lunar(ct)
    print(('公历 {}  北京时间 {}'.format(ln.localtime.date(), ln.localtime.time())))
    '''
    print('{} 【{}】 {}年 {}日 {}时'.format(ln.ln_date_str(),
                                       ln.gz_year(),
                                       ln.sx_year(),
                                       ln.gz_day(),
                                       ln.gz_hour()))
    print('节气：{}'.format(ln.ln_jie()))
    '''
    print(ln.ln_date())


ct = datetime.datetime(2015, 2, 19, 13, 0, 15) 
test(ct)   
#if __name__ == '__main__':
"""
"""
sort_results_path = 'C:/Users/Administrator/stockPriditionProjects/data/601336sort_results.csv'
from data_preprocess import preprocess
N = 60
aa,bb = preprocess.get_last_N_days_data_for_MLP(code,N)
print(aa[1])

import tushare as ts
df = ts.get_hist_data(code)
df = df.head(1)
print(df)
print(df.columns.tolist())
#dtime = df.set_index('time')
#price = dtime['price']
Df = ts.get_tick_data(code, date)
print(Df.columns.tolist())
"""
"""
X, y = load_data.To_DL_datatype(code)
X = preprocessing.scale(X)
y = preprocessing.scale(y)
X_train, X_test, Y_train, Y_test = load_data.create_Xt_Yt(X, y, 0.8)
X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))
"""


"""
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.pylab import date2num
import datetime
hist_data = ts.get_hist_data('601558')
# 对tushare获取到的数据转换成candlestick_ohlc()方法可读取的格式
data_list = []
for dates,row in hist_data.iterrows():
    # 将时间转换为数字
    date_time = datetime.datetime.strptime(dates,'%Y-%m-%d')
    t = date2num(date_time)
    Open,high,close,low = row[:4]
    datas = (t,Open,high,low,close)
    data_list.append(datas)

data_list = data_list[:20]
# 创建子图
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
# 设置X轴刻度为日期时间
ax.xaxis_date()
plt.xticks(rotation=45)
plt.yticks()
plt.title("股票代码：601558两年K线图")
plt.xlabel("时间")
plt.ylabel("股价（元）")
mpf.candlestick_ohlc(ax,data_list,width=0.5,colorup='r',colordown='g')
plt.grid()
plt.show()
plt.savefig('C:/Users/Administrator/stockPriditionProjects/data/601558_k_line.jpg')

if __name__ == '__main__':
    plt.show()
    plt.savefig('C:/Users/Administrator/stockPriditionProjects/data/601558_k_line.jpg')
"""   
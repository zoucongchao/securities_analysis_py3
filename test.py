# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 16:53:44 2018

@author: Administrator
"""

from data_preprocess import load_data
path = 'C:/Users/Administrator/stockPriditionProjects/data/601336.csv'
code = '601336'


aa,bb,cc,dd,ee,ff,gg,hh,ii,jj,kk,ll = load_data.load_fq_ma5_ma10_ma20_ma30_ma60_ma120_ma250_ma500_from_tushare(code)
print(aa[0])
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
        
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import time
import os
import glob
import re
import datetime as dt

def tst(n):
    path = '/home/douglas/Documentos/pesquisa/7GHz/arquivos/'
    last_files = [file for file in glob.glob(os.path.join(path ,'*'))]
    last_files.sort(key=os.path.getmtime)
    f=open(last_files[n])
    h=f.readlines(3)
    data = pd.read_csv(last_files[n], delim_whitespace= True, names=['R','L'],na_filter=True )
    kk=data.R[0:3]
    idx=data[(data['R'] ==kk[0]) | (data['R'] ==kk[1])| (data['R'] ==kk[2])].index.tolist()
    idx2=data[(data['R'] ==kk[1])].index.tolist()
    if len(idx2) >1:
        for i in range(len(idx2)):
            j = (i*3)+2
            if i != len(idx2)-1:
                if i == 0:
                    d = data.loc[idx[j]+1:idx[j+1]-1]
                    d.index =  pd.date_range(data.R[idx2[i]][10:]+' '+data.L[idx2[i]], periods=len(d), freq='20 ms',dayfirst=True)
                    p=pd.concat([d])
                else:
                    print 'jj'
                    di = data.loc[idx[j]+1:idx[j+1]-1]
                    di.index =  pd.date_range(data.R[idx2[i]][10:]+' '+data.L[idx2[i]], periods=len(di), freq='20 ms',dayfirst=True)
                    p=pd.concat([p,di])  
            else:
                d_i = data.loc[idx[j]+1:]
                d_i.index =  pd.date_range(data.R[idx2[i]][10:]+' '+data.L[idx2[i]], periods=len(d_i), freq='20 ms',dayfirst=True)
                p=pd.concat([p,d_i])
        d=p
    else:
        data = pd.read_csv(last_files[n], skiprows=[0,1,2],delim_whitespace= True, names=['R','L'],na_filter=True )
        data.index = pd.date_range(h[1][10::], periods = len(data) ,freq='20 ms',dayfirst=True)
        d=data
    
    d['R']=np.float_(d.R)
    d['L']=np.float_(d.L)
    tt=h[1][10::]
    print ''
    print 'deseja salva os dados '
    print 'Y ', 'or ', 'N '
    ll=raw_input()
    if ll== 'y' or  ll == 'Y':
	d.to_csv(last_files[n][57::]+'.dat', sep='\t')
    else:
	print 'ok'	
    print 'deseja integrar'
    print 'Y', 'or', 'N'
    j=raw_input()
    if j == 'y' or  j == 'Y':
	print 'quantos minutos'
	mm=raw_input()
	mms=str(mm)
        d_1m=d.resample(mms).mean()
        des_1m=d.resample(mms).std()
        return d_1m,tt,des_1m
    else:
        return d,tt
#-------------------------------------------------------------------------------------------------

def read_gato():
    path = '/home/douglas/Documentos/pesquisa/7GHz/arquivos/'
    last_files = [file for file in glob.glob(os.path.join(path ,'*'))]
    last_files.sort(key=os.path.getmtime)
    for i in range(len(last_files)):
        print i, ' ',last_files[i][33::]
    print ''
    print 'Esconlha o indice relacionado a data de interesse' 	
    print ''
    

def read_teste(n):
    print n, ' ',last_files[n][33::]
    f=open(last_files[n])
    h=f.readlines(3)
    data = pd.read_csv(last_files[n], delim_whitespace= True, names=['R','L'],na_filter=True )
    kk=data.R[0:3]
    idx=data[(data['R'] ==kk[0]) | (data['R'] ==kk[1])| (data['R'] ==kk[2])].index.tolist()
    idx2=data[(data['R'] ==kk[1])].index.tolist()
    print len(idx2) 


#------------------------------------------------------------------------------------
#=====================rotinas de plotagem============================================
#------------------------------------------------------------------------------------
def compare_2_plot_data(d,tt,d2,tt2):
    plt.rcParams['figure.figsize'] = 10,8
    figure1, (ax,ax1) = plt.subplots(2,sharex=False,sharey=False)
    #figure1, ax = plt.subplots()
    ax.plot(d['L']+2,COLOR='b',label='Left')
    #ax.plot(d2['R'].shift(2,'D'),color='g',label='Right')
    ax.plot(d2['L'],color='g',label='Left')
    legend = ax.legend(loc='upper left',frameon=False)
    # ax.set_xlim(h[1][10::],datepf)
    ax.set_ylim(0,10)
    ax.set_title(tt)
    ax.set_ylabel('Relative Units (Volts)')
    ax.set_xlabel('UT')
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax1.plot(d['R'],COLOR='b',label='Right')
    #ax.plot(d['R'].shift(0,'D'),color='r',label='Right')
    ax1.plot(d2['R'],color='r',label='Right')
    legend = ax1.legend(loc='upper left',frameon=False)
    # ax.set_xlim(h[1][10::],datepf)
    ax1.set_ylim(0,10)
    ax1.set_title(tt2)
    ax1.set_ylabel('Relative Units (Volts)')
    ax1.set_xlabel('UT')
    ax1.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    if tt[0:9] == '2/26/2017':
        ax.plot([dt.datetime(2017,2,26,9,54),dt.datetime(2017,2,26,9,54)],[-10,10],lw=5,color='pink',ls='--')
        ax.plot([dt.datetime(2017,2,26,13,2),dt.datetime(2017,2,26,13,2)],[-10,10],lw=3,color='black',ls='--')
        ax.text(dt.datetime(2017,2,26,13,2),4,' Inicio eclipse')
        ax.text(dt.datetime(2017,2,26,14,30),4,'  Maximo eclipse')
        ax.plot([dt.datetime(2017,2,26,14,30),dt.datetime(2017,2,26,14,30)],[-10,10],lw=3,color='black',ls='--')

    ax.grid()

def plot_data(d,tt):
    plt.rcParams['figure.figsize'] = 10,8
    figure1, ax = plt.subplots()
    ax.plot(d['L'],COLOR='b',label='Left')
    ax.plot(d['R'],color='r',label='Right')
    legend = ax.legend(loc='upper left',frameon=False)
    # ax.set_xlim(h[1][10::],datepf)
    ax.set_ylim(0,10)
    ax.set_title(tt)
    ax.set_ylabel('Relative Units (Volts)')
    ax.set_xlabel('UT')
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    if tt[0:9] == '2/26/2017':
        ax.plot([dt.datetime(2017,2,26,9,54),dt.datetime(2017,2,26,9,54)],[-10,10],lw=5,color='pink',ls='--')
        ax.plot([dt.datetime(2017,2,26,13,2),dt.datetime(2017,2,26,13,2)],[-10,10],lw=3,color='black',ls='--')
        ax.text(dt.datetime(2017,2,26,13,2),4,' Inicio eclipse')
        ax.text(dt.datetime(2017,2,26,14,30),4,'  Maximo eclipse')
        ax.plot([dt.datetime(2017,2,26,14,30),dt.datetime(2017,2,26,14,30)],[-10,10],lw=3,color='black',ls='--')
    ax.grid()


def R_L_2_plot_data(d,tt,d2,tt2):
    sft=np.abs(np.float(tt[2:4])-np.float(tt2[2:4]))
    plt.rcParams['figure.figsize'] = 10,8
    figure1, (ax,ax1) = plt.subplots(2,sharex=False,sharey=False)
    #figure1, ax = plt.subplots()
    ax.plot(d['L']+1,COLOR='b',label=('Left '+tt[0:9]))
    ax.plot(d2['L'].shift(sft,'D')+1,color='g',label=('Left '+tt2[0:9]))
    ax1.plot(d['R'],color='b',label=('Right '+tt[0:9]))
    ax1.plot(d2['R'].shift(sft,'D'),color='g',label=('Right '+tt2[0:9]))
    legend = ax.legend(loc='upper left',frameon=False)
    # ax.set_xlim(h[1][10::],datepf)
    ax.set_ylim(0,10)
    ax.set_title(tt)
    ax.set_ylabel('Relative Units (Volts)')
    ax.set_xlabel('UT')
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax1.set_ylim(0,10)
    ax1.set_title(tt2)
    ax1.set_ylabel('Relative Units (Volts)')
    ax1.set_xlabel('UT')
    ax1.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    legend = ax1.legend(loc='upper left',frameon=False)
    if tt[0:9] == '2/26/2017':
        ax.plot([dt.datetime(2017,2,26,9,54),dt.datetime(2017,2,26,9,54)],[-10,10],lw=5,color='pink',ls='--')
        ax.plot([dt.datetime(2017,2,26,13,2),dt.datetime(2017,2,26,13,2)],[-10,10],lw=3,color='black',ls='--')
        ax.text(dt.datetime(2017,2,26,13,2),6,' Inicio eclipse')
        ax.text(dt.datetime(2017,2,26,14,30),7,'  Maximo eclipse')
        ax.plot([dt.datetime(2017,2,26,14,30),dt.datetime(2017,2,26,14,30)],[-10,10],lw=3,color='black',ls='--')
        ax.text(dt.datetime(2017,2,26,15,55),6,'  Fim eclipse')
        ax.plot([dt.datetime(2017,2,26,15,55),dt.datetime(2017,2,26,15,55)],[-10,10],lw=3,color='black',ls='--')
        ax1.plot([dt.datetime(2017,2,26,9,54),dt.datetime(2017,2,26,9,54)],[-10,10],lw=5,color='pink',ls='--')
        ax1.plot([dt.datetime(2017,2,26,13,2),dt.datetime(2017,2,26,13,2)],[-10,10],lw=3,color='black',ls='--')
        ax1.text(dt.datetime(2017,2,26,13,2),6,' Inicio eclipse')
        ax1.text(dt.datetime(2017,2,26,14,30),7,'  Maximo')
        ax1.plot([dt.datetime(2017,2,26,14,30),dt.datetime(2017,2,26,14,30)],[-10,10],lw=3,color='black',ls='--')
        ax1.text(dt.datetime(2017,2,26,15,55),6,'  Fim ')
        ax1.plot([dt.datetime(2017,2,26,15,55),dt.datetime(2017,2,26,15,55)],[-10,10],lw=3,color='black',ls='--')
    ax.grid()

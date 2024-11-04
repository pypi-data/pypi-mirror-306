#!/usr/bin/env python
# coding: utf-8


import math  
import tushare as ts  
import pandas as pd  
import numpy as np  
import os  

import sys
import requests
import json
from datetime import datetime, timedelta  
  


print("Risk Control V4.0 v20241104")
print("---------------------------------------------------------------------------------------------")
print("Reduce the risk, but also reduce the profit.")
print("Methon:")
print("	1-Many codes")
print("	2-Test_mode")
print("	3-Shift to Current Mode")
print("	4-Get NOW  -ALL")
print("	5-Test -ALL")
global currentmode
global SZ_ZS
currentmode=0
m=input("\nPlease input the Code(1/2/3 or code):")



# 设置tushare token  
ts.set_token('7543479e39691641caa318f78cc96979cacdf67d5a746b65aa20b306')
 
# 初始化pro接口  
pro = ts.pro_api()  


#日志文件(暂不启用）
file = open("inf.txt", 'w').close()  
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
        #可以选择"w"
        self.log = open(filename, "a", encoding="utf-8")  # 防止编码错误
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        pass
    def reset(self):
        self.log.close()
        sys.stdout=self.terminal
def printinf(a,*b):
	sys.stdout = Logger('inf.txt') 
	print(a,*b)
	sys.stdout.reset()
	
def get_current(data,r):
	'''获取实时股票数据'''
	global SZ_ZS
	print(r)
	
	dfnow = ts.get_realtime_quotes([r])[["code","date","open","high","low","price","pre_close","name","bid","volume","amount"]]

	dfnow = dfnow.rename(columns={"code": "ts_code"})   
	dfnow = dfnow.rename(columns={"date": "trade_date"}) 	
	dfnow = dfnow.rename(columns={"price": "close"}) 
	dfnow = dfnow.rename(columns={"name": "change"}) 
	dfnow = dfnow.rename(columns={"bid": "pct_chg"}) 
	dfnow = dfnow.rename(columns={"volume": "vol"}) 
	dfnow["trade_date"]=dfnow["trade_date"].str.replace("-","")
	dfnow["trade_date"]=dfnow["trade_date"].str.replace("-","")	
	dfnow["open"]=dfnow["open"].astype(float)
	dfnow["close"]=dfnow["close"].astype(float)
	dfnow["high"]=dfnow["high"].astype(float)
	dfnow["low"]=dfnow["low"].astype(float)		
	dfnow["pre_close"]=dfnow["pre_close"].astype(float)		
	dfnow["vol"]=dfnow["vol"].astype(float)/100	
	dfnow["amount"]=dfnow["amount"].astype(float)	

		
	dfnow["change"]=dfnow["close"]-dfnow["open"]
	dfnow["pct_chg"]=dfnow["change"]/dfnow["pre_close"]	
	data=pd.concat([dfnow,data], ignore_index=True).reset_index(drop=True)	
	#print(len(data))
	print(data.head(5))
	return data	
    
def getHistoryData(market, number, start_data, end_data):
# market: 0:沪市 1:深市
# number: 股票代码
# start_data: 起始日期:yyyymmdd
# end_data: 结束时间:yyyymmdd
    print('getHistoryData...')
    url='http://yunhq.sse.com.cn:32041/v1/sh1/dayk/000001?callback=jQuery111208282462776376776_1569062885488&select=ts_code%2Cdate%2Copen%2Chigh%2Clow%2Cclose%2Cpre_close%2Cchange%2Cpct_chg%2Cvolume%2Camount&begin=-2000&end=-1&_=1569062885522'
    response=requests.get(url,headers={'Referer': 'http://www.sse.com.cn/market/price/trends/'})
    json_str=response.text[42:-1]
    data=json.loads(json_str)
    kline=data['kline']
    kline2=pd.DataFrame(kline,columns=["ts_code","trade_date","open","high","low","close","pre_close","change","pct_chg","vol","amount"]).sort_values(by=["trade_date"],ascending=False,na_position="last")

    kline2=kline2.reset_index(drop=True)

    return kline2	
          
def get_stock_data(stock_code, start_date='20200101', end_date=''):  
    '''获取股票数据，并保存为csv文件。'''
    # 定义数据保存目录  
    stock_dir = 'stock'  
    if not os.path.exists(stock_dir):  
        os.makedirs(stock_dir)  
      
    # 将日期格式转换为YYYYMMDD形式，如果end_date为空则使用当前日期  
    if not end_date:  
        end_date = datetime.now().strftime('%Y%m%d')  
    start_date_str = start_date.replace('-', '')  # 如果输入的日期格式为YYYY-MM-DD，则需要替换掉'-'  
    end_date_str = end_date.replace('-', '')     # 同上，处理end_date的格式  
      
    # 构造文件名 
    if  currentmode==1: 
        filename = f'{stock_code}_{start_date_str}_{end_date_str}_c.csv'  #实时文件加C
        filepath = os.path.join(stock_dir, filename)  
    else:
        filename = f'{stock_code}_{start_date_str}_{end_date_str}.csv'  
        filepath = os.path.join(stock_dir, filename)    
      
    # 检查文件是否存在  
    if os.path.exists(filepath) and currentmode!=1:  
        # 如果文件存在，则直接加载数据  
        df = pd.read_csv(filepath, index_col=0, parse_dates=True)  
        print("直接使用源文件："+filepath)
        
    elif stock_code=="szzs":
        df = getHistoryData('0', '000001', start_date, end_date)
        df['trade_date']=df['trade_date'].astype(str).str[:8]  
        df['trade_date'] = pd.to_datetime(df['trade_date'])  
        df.set_index('trade_date', inplace=True)  
        df.sort_index(inplace=True)
        df.to_csv(filepath)
    else:  
        # 如果文件不存在，则下载数据  
        df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)  
        if currentmode==1:
            try:
                df=get_current(df,stock_code.replace(".SH",""))
            except:
                df=get_current(df,stock_code.replace(".SZ",""))       
        
        df['trade_date'] = pd.to_datetime(df['trade_date'])  
        df.set_index('trade_date', inplace=True)  
        df.sort_index(inplace=True)  
          
        # 保存数据到文件  
        df.to_csv(filepath)  
      
    return df  


   
def calculate_ma(data, window_sizes=[5, 10, 20, 30]):  
    '''计算移动平均线'''
    for window in window_sizes:  
        data[f'ma{window}'] = data['close'].rolling(window=window).mean()  
    return data  
  

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):  
    '''计算MACD'''    
    data['ema12'] = data['close'].ewm(span=short_window, adjust=False).mean()  
    data['ema26'] = data['close'].ewm(span=long_window, adjust=False).mean()  
    data['diff'] = data['ema12'] - data['ema26']  
    data['dea'] = data['diff'].ewm(span=signal_window, adjust=False).mean()  
    data['macd'] = 2 * (data['diff'] - data['dea'])  
    return data  
  
#暂时没有用到
def calculate_kdj(stock_data, n=9, m1=3, m2=3):  
    '''计算KDJ'''       
    # 计算RSV（未成熟随机值）  
    stock_data['LowList'] = stock_data['low'].rolling(window=n, min_periods=1).min()  
    stock_data['HighList'] = stock_data['high'].rolling(window=n, min_periods=1).max()  
    stock_data['RSV'] = (stock_data['close'] - stock_data['LowList']) / (stock_data['HighList'] - stock_data['LowList']) * 100  
    stock_data['RSV']=stock_data['RSV'].fillna(50)  # 如果HighList和LowList相等，则RSV设为50  
      
    # 计算K值、D值  
    stock_data['K'] = pd.DataFrame(stock_data['RSV']).ewm(span=m1, adjust=False).mean()  
    stock_data['D'] = stock_data['K'].ewm(span=m2, adjust=False).mean()  
    stock_data['J'] = 3 * stock_data['K'] - 2 * stock_data['D']  
      
    return stock_data  
  

def calculate_rsi(data, n=14):  
    '''计算RSI''' 
    delta = data['close'].diff()  
    gain = delta.where(delta > 0, 0)  
    loss = -delta.where(delta < 0, 0)  
    avg_gain = gain.rolling(window=n, min_periods=1).mean()  
    avg_loss = loss.rolling(window=n, min_periods=1).mean()  
    rs = avg_gain / avg_loss  
    data['RSI'] = 100 - (100 / (1 + rs))  
    return data  
  
  
def calculate_bollinger(data, window=20): 
    '''计算布林带''' 
    rolling_mean = data['close'].rolling(window=window).mean()  
    rolling_std = data['close'].rolling(window=window).std()  
    data['bollinger_upper'] = rolling_mean + (rolling_std * 2)  
    data['bollinger_lower'] = rolling_mean - (rolling_std * 2)  
    return data  

def calculate_wr(stock_data, n=10): 
    '''计算威廉指标WR'''    
    stock_data['HighList'] = stock_data['high'].rolling(window=n, min_periods=1).max()  
    stock_data['LowList'] = stock_data['low'].rolling(window=n, min_periods=1).min()  
    stock_data['WR'] = (stock_data['HighList'] - stock_data['close']) / (stock_data['HighList'] - stock_data['LowList']) * 100  
      
    return stock_data  

  
def calculate_vol_change(data):  
    '''计算成交量变化百分比'''  
    data['vol_change_pct'] = data['vol'].pct_change() * 100  
    return data  


##############################################################


    
def calculate_score(df):  
	'''计算打分'''
     
	print('目前用的规则：测试规则-MA MACD-DIF 100%-50%-0%+止盈+vol,版本：20241031')     
	df=df.reset_index()
	df['ori_value'] = 0.00
	df["score"]=0
	df["record"]=""
	df["record2"]=""
	macfac=0

	for ids,cols in df.iterrows():
		
		if ids==0:
			continue
            



		if  cols["ma5"]>cols["ma10"] and cols["ma10"]>cols["ma20"] and cols["ma20"]>cols["ma30"]:
			df.loc[ids,"score"]=100
			df.loc[ids,"record"]="100%:MA-GOOD；"

			    
		elif  cols["ma5"]<cols["ma10"] and cols["ma10"]<cols["ma20"] and cols["ma20"]<cols["ma30"]:
			df.loc[ids,"score"]=0
			df.loc[ids,"record"]="0%:MA-BAD；"
		
        #其他情况的原则
		elif cols["macd"]>macfac and cols["diff"]>macfac :
			df.loc[ids,"score"]=100
			df.loc[ids,"record"]="100%:MACD AND DIF IS GOOD；"
            
		elif cols["macd"]>macfac and cols["diff"]<macfac :
			df.loc[ids,"score"]=50
			df.loc[ids,"record"]="50%: MACD IS GOOD BUT DIF IS NOT GOOD；"
            
		

				    
		else:
			df.loc[ids,"score"]=0	
			df.loc[ids,"record"]="0%: TREAD NOT GOOD；"		
			
		if cols['macd']>=0 and df.loc[ids-1,"macd"]<0:
			 df.loc[ids,"record2"]='●'
		elif  cols['macd']>=0 and cols['macd']>df.loc[ids-1,"macd"]:
			 df.loc[ids,"record2"]=df.loc[ids-1,"record2"]+'+'		
		elif  cols['macd']>=0 and cols['macd']<df.loc[ids-1,"macd"]:
			 df.loc[ids,"record2"]=df.loc[ids-1,"record2"]+'-'
			 	
		#各种金叉的提醒	

		if  (cols["ma10"]==cols["ma20"]) and (cols["ma10"]>df.loc[ids-1,"ma10"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"❤MA:Gold(10=20), "
		if  (cols["ma20"]==cols["ma30"]) and (cols["ma20"]>df.loc[ids-1,"ma20"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"❤MA:Gold(20=30), "
		if (cols["ma5"]==cols["ma10"]) and (cols["ma5"]>df.loc[ids-1,"ma5"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"MA:❤Gold(5=10), "		
		if (cols["macd"]==macfac and cols["macd"]>df.loc[ids-1,"macd"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"❤Gold,macd=0; "	
		if (cols["diff"]==0 and cols["diff"]<df.loc[ids-1,"diff"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"●dead,dif=0; "					
						

		#成交量的风控(仅提醒）
		if cols['vol_change_pct']>50:
			df.loc[ids,"record"]="●vol!; "+df.loc[ids,"record"]		

		#(仅提醒）
		df.loc[ids,"record"]=df.loc[ids,"record"]+"-----ma5("+str(round(df.loc[ids,'ma5'],2))+"),ma10("+str(round(df.loc[ids,'ma10'],2))+"),ma20("+str(round(df.loc[ids,'ma20'],2))+"),ma30("+str(round(df.loc[ids,'ma30'],2))+"),dif:"+str(round(df.loc[ids,'diff'],2))+",macd:"+str(round(df.loc[ids,'macd'],2))+','


		#增加止盈（叠加天量,目前仅提醒,测试结果良好）
		if 1== 1:
			i=ids
			if i==0:
				df.loc[i,'ori_value'] = df.loc[i, 'close']
			if df.loc[i, 'score']>0 and df.loc[i-1, 'score']==0:
				df.loc[i,'ori_value'] = df.loc[i-1, 'close']  
			if df.loc[i, 'score']>0  and df.loc[i-1, 'score']!=0:        
				df.loc[i,'ori_value'] = df.loc[i-1, 'ori_value']  
			if df.loc[i, 'score']>0:
				targets=round((df.loc[i, 'close']-df.loc[i, 'ori_value'])/df.loc[i, 'ori_value'],2)
				if targets>=0.20:
					df.loc[i, 'score']=df.loc[i, 'score']*0.5
					df.loc[i,"record"]="止盈("+str(targets)+')'+df.loc[ids,"record"]
				if targets>=0.20 and cols['vol_change_pct']>50: 
					df.loc[i, 'score']=df.loc[i, 'score']*0.5
					df.loc[i,"record"]="止盈("+str(targets)+')'+df.loc[ids,"record"]
				
			
	return df  


def NO_CONTROL_calculate_score(df):  #
	'''计算打分-测试版'''     
	df=df.reset_index()
	df["score"]=100    
	df.loc[0,"score"]=0
	df["record"]="FULL"
	macfac=0

	return df  


def macd_dif_calculate_score(df): # 
	'''计算打分-MACD-DIF'''
	print('目前用的规则：MACD-DIF-100%-50%-0%')     
	df=df.reset_index()
	df["score"]=0
	df["record"]=""
	macfac=0

	for ids,cols in df.iterrows():
		
		if ids==0:
			continue
        
			
		#其他情况用MACD和DIF控制
		if cols["macd"]>0 and cols["diff"]>0:
			df.loc[ids,"score"]=100
			df.loc[ids,"record"]="100%:   MACD AND DIF IS GOOD；"
		elif cols["macd"]>0 and cols["diff"]<0:
			df.loc[ids,"score"]=50
			df.loc[ids,"record"]="50%:   MACD<0 BUT DIF<0；"		
        		    
		else:
			df.loc[ids,"score"]=0
			df.loc[ids,"record"]="0%:   TREAD NOT GOOD；"		
			
			
		#各种金叉的提醒	

		if  (cols["ma10"]==cols["ma20"]) and (cols["ma10"]>df.loc[ids-1,"ma10"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"❤MA:Gold(10=20), "
		if  (cols["ma20"]==cols["ma30"]) and (cols["ma20"]>df.loc[ids-1,"ma20"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"❤MA:Gold(20=30), "
		if (cols["ma5"]==cols["ma10"]) and (cols["ma5"]>df.loc[ids-1,"ma5"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"MA:❤Gold(5=10), "		
		if (cols["macd"]==macfac and cols["macd"]>df.loc[ids-1,"macd"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"❤Gold,macd=0; "	
		if (cols["diff"]==0 and cols["diff"]<df.loc[ids-1,"diff"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"●dead,dif=0; "					
						

		#成交量的风控(仅提醒）
		if cols['vol_change_pct']>50:
			df.loc[ids,"record"]="●vol!; "+df.loc[ids,"record"]		

		#(仅提醒）
		df.loc[ids,"record"]=df.loc[ids,"record"]+"-----ma5("+str(round(df.loc[ids,'ma5'],2))+"),ma10("+str(round(df.loc[ids,'ma10'],2))+"),ma20("+str(round(df.loc[ids,'ma20'],2))+"),ma30("+str(round(df.loc[ids,'ma30'],2))+"),dif:"+str(round(df.loc[ids,'diff'],2))+",macd:"+str(round(df.loc[ids,'macd'],2))+','
		
	return df  


def WORK_calculate_score(df):  
	'''计算打分'''     
	print('目前用的规则：MA MACD-DIF 100%-50%-0%+止盈+vol')     
	df=df.reset_index()
	df['ori_value'] = 0
	df["score"]=0
	df["record"]=""
	macfac=0

	for ids,cols in df.iterrows():
		
		if ids==0:
			continue
            



		if  cols["ma5"]>cols["ma10"] and cols["ma10"]>cols["ma20"] and cols["ma20"]>cols["ma30"]:
			df.loc[ids,"score"]=100
			df.loc[ids,"record"]="100%:MA-GOOD；"

			    
		elif  cols["ma5"]<cols["ma10"] and cols["ma10"]<cols["ma20"] and cols["ma20"]<cols["ma30"]:
			df.loc[ids,"score"]=0
			df.loc[ids,"record"]="0%:MA-BAD；"
		
        #其他情况的原则
		elif cols["macd"]>macfac and cols["diff"]>macfac :
			df.loc[ids,"score"]=100
			df.loc[ids,"record"]="100%:MACD AND DIF IS GOOD；"
            
		elif cols["macd"]>macfac and cols["diff"]<macfac :
			df.loc[ids,"score"]=50
			df.loc[ids,"record"]="50%: MACD IS GOOD BUT DIF IS NOT GOOD；"
            
		

				    
		else:
			df.loc[ids,"score"]=0	
			df.loc[ids,"record"]="0%: TREAD NOT GOOD；"		
			
			
		#各种金叉的提醒	

		if  (cols["ma10"]==cols["ma20"]) and (cols["ma10"]>df.loc[ids-1,"ma10"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"❤MA:Gold(10=20), "
		if  (cols["ma20"]==cols["ma30"]) and (cols["ma20"]>df.loc[ids-1,"ma20"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"❤MA:Gold(20=30), "
		if (cols["ma5"]==cols["ma10"]) and (cols["ma5"]>df.loc[ids-1,"ma5"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"MA:❤Gold(5=10), "		
		if (cols["macd"]==macfac and cols["macd"]>df.loc[ids-1,"macd"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"❤Gold,macd=0; "	
		if (cols["diff"]==0 and cols["diff"]<df.loc[ids-1,"diff"]):
			df.loc[ids,"record"]=df.loc[ids,"record"]+"●dead,dif=0; "					
						

		#成交量的风控(仅提醒）
		if cols['vol_change_pct']>50:
			df.loc[ids,"record"]="●vol!; "+df.loc[ids,"record"]		

		#(仅提醒）
		df.loc[ids,"record"]=df.loc[ids,"record"]+"-----ma5("+str(round(df.loc[ids,'ma5'],2))+"),ma10("+str(round(df.loc[ids,'ma10'],2))+"),ma20("+str(round(df.loc[ids,'ma20'],2))+"),ma30("+str(round(df.loc[ids,'ma30'],2))+"),dif:"+str(round(df.loc[ids,'diff'],2))+",macd:"+str(round(df.loc[ids,'macd'],2))+','


		#增加止盈（叠加天量,目前仅提醒,测试结果良好）
		if 1== 1:
			i=ids
			if i==0:
				df.loc[i,'ori_value'] = df.loc[i, 'close']
			if df.loc[i, 'score']>0 and df.loc[i-1, 'score']==0:
				df.loc[i,'ori_value'] = df.loc[i-1, 'close']  
			if df.loc[i, 'score']>0  and df.loc[i-1, 'score']!=0:        
				df.loc[i,'ori_value'] = df.loc[i-1, 'ori_value']  
			if df.loc[i, 'score']>0:
				targets=round((df.loc[i, 'close']-df.loc[i, 'ori_value'])/df.loc[i, 'ori_value'],2)
				if targets>=0.20:
					df.loc[i, 'score']=df.loc[i, 'score']*0.5
					df.loc[i,"record"]="止盈("+str(targets)+')'+df.loc[ids,"record"]
				if targets>=0.20 and cols['vol_change_pct']>50: 
					df.loc[i, 'score']=df.loc[i, 'score']*0.5
					df.loc[i,"record"]="止盈("+str(targets)+')'+df.loc[ids,"record"]
				
			
	return df  



def calculate_position_pct(score): 
    '''定义函数来计算仓位'''  
    return score/100  
    
    #if 60 <= score < 80:  
    #    return 0.50    
    #elif score >= 80:  
    #    return 1.00  
    #else:  
    #    return 0.0  

def backtest_strategy(df):  
    """  
    根据score进行回测，并更新DataFrame。  
    :param df: 包含'close'和'score'列的DataFrame。  
    :return: 更新后的DataFrame，包含回测结果。
    使用的是当天收盘价,买卖。  
    """  
      
    # 初始化变量和列  
    if df['open'][3]>1000:
        initial_cash = 100000000 #对于上证指数设置初始1个亿，以防有较多的灵股数不足误差。  
    else:
        initial_cash = 1000000 #以防有较多的灵股数不足误差。          
    cash = initial_cash  
    position = 0   
    #df['no']=0
    df['buy'] = 0  
    df['sell'] = 0  
    df['hold'] = 0  
    df['stock_value'] = 0  
    df['cash'] = initial_cash  
    df['pnl'] = 0  
    df['position_pct'] = df['score'].apply(lambda score: calculate_position_pct(score))  
    df['total_value'] = initial_cash  
    
    df['stock_value'] = df['stock_value'].astype(float)  
    df['cash'] = df['cash'].astype(float)  
    df['pnl'] = df['pnl'].astype(float)  
    df['total_value'] = df['total_value'].astype(float)

    
          
    # 回测逻辑  
    for i in range(1, len(df)):  
        # 计算目标持仓数量（如果分数不变动不用计算）
        
        
        
        if df.loc[i, 'position_pct']!=df.loc[i-1, 'position_pct']:    
            target_stock_value = (cash+position * df.loc[i, 'close']) * df.loc[i, 'position_pct']  
            target_position = target_stock_value / df.loc[i, 'close']  
        else:  
            target_position=position 
        # 如果需要调整为100的倍数，则使用以下代码（但请注意，这可能会引入不必要的交易噪声）  
        adjusted_target_position = int(target_position // 100) * 100  # 这里使用了整除来确保是100的倍数  
          
        # 计算买卖数量  
        buy = max(adjusted_target_position - position, 0)  
        sell = max(position - adjusted_target_position, 0)  
          
        # 执行交易操作  
        if sell > 0:  
            cash += sell * df.loc[i, 'close']  # 卖出股票，增加现金  
            position -= sell  # 更新持仓数量  
          
        if buy > 0 and cash >= buy * df.loc[i, 'close']:  # 确保有足够的现金购买股票  
            cash -= buy * df.loc[i, 'close']  # 买入股票，减少现金  
            position += buy  # 更新持仓数量  
        # 如果现金不足，则buy操作已经被上面的if条件阻止，因此不需要额外的else语句将buy设置为0。  
          
        # 更新DataFrame中的相关列  
        df.loc[i, 'buy'] = buy  
        df.loc[i, 'sell'] = sell  
        df.loc[i, 'hold'] = position  
        df.loc[i, 'stock_value'] = position * df.loc[i, 'close']  # 更新持仓价值  
        df.loc[i, 'cash'] = cash  # 更新现金余额  
        df.loc[i, 'pnl'] = (position * df.loc[i, 'close'] + cash) - df.loc[i-1, 'total_value'] if i > 0 else 0  # 计算盈亏（当前总价值减去前一天的总价值）  
        df.loc[i, 'total_value'] = position * df.loc[i, 'close'] + cash  # 计算当前总价值（持仓价值加现金）  
        

                    
    return df.reset_index(drop=True)  # 重置索引并删除旧索引列（如果需要的话）
  



  
def trimmed_mean(series):  

    try:  
        series = series.dropna()  # 去除NaN值  
        if len(series) <= 2:  
            return np.nan  # 如果列中元素不足3个，则返回NaN  
        return series.sort_values()[2:-1].mean()  # 计算去除最大最小后的平均值  (同时去除第一个指数项目)
    except Exception as e:  
        # 可以选择性地打印错误信息，但在生产代码中通常应该避免打印  
        #print(f"Error calculating trimmed mean for series: {e}")  
        return np.nan  # 出现错误时返回NaN


def mark_stocks(df):  
    # 计算total_value, MAXvalue, MINvalue在第二行到倒数第二行之间的平均数  
    # 注意：这里我们假设第一行是标题行（header），所以不需要包括在内  
    # 同时，我们也假设最后一行不需要包括在内进行计算平均数  
    #valid_rows = df.iloc[1:-1]
    avg_total_value = df['total_value'].sort_values()[2:-1].mean()
    avg_max_value = df['MAXvalue'].sort_values()[2:-1].mean()
    avg_min_value = df['MINvalue'].sort_values()[2:-1].mean() 

    q75_total_value = df['total_value'].sort_values()[2:-1].quantile(0.75)  
    q75_max_value = df['MAXvalue'].sort_values()[2:-1].quantile(0.75)  
    q75_min_value = df['MINvalue'].sort_values()[2:-1].quantile(0.75) 

      
    # 遍历第二行到倒数第二行的数据（注意索引从1开始，因为0是标题行）  
    for index in range(1, len(df) - 1):  
        row = df.iloc[index]  
        
        if (row['total_value'] > q75_total_value and  
            row['MAXvalue'] > q75_max_value and  
            row['MINvalue'] > q75_min_value):  
            # 在StockName前面追加上!!!标记  
            df.at[index, 'StockName'] = '●' + row['StockName']  
        if (row['total_value'] > avg_total_value and  
            row['MAXvalue'] > avg_max_value and  
            row['MINvalue'] > avg_min_value):  
            # 在StockName前面追加上!!!标记  
            df.at[index, 'StockName'] = '●' + row['StockName']              
            
        elif (row['total_value'] < avg_total_value and  
            row['MAXvalue'] < avg_max_value and  
            row['MINvalue'] < avg_min_value):  
            # 在StockName前面追加上!!!标记  
            df.at[index, 'StockName'] = '!' + row['StockName']        
    return df 
 
def main(stock_dict, start_date, end_date):   
    summary_data = pd.DataFrame()  # 用于汇总每个股票结果的DataFrame  
    output_dir='file'  
    
    if not os.path.exists(output_dir):  
        os.makedirs(output_dir)  
        
    for stock_name, stock_code in stock_dict.items():  
        output_file=os.path.join(output_dir,f"{stock_name}_stock_data.xlsx")

        stock_data = get_stock_data(stock_code, start_date, end_date)    
          
        # 计算移动平均线  
        stock_data = calculate_ma(stock_data)  
          
        # 计算MACD  
        stock_data = calculate_macd(stock_data)  
          
        # 计算KDJ  
        stock_data = calculate_kdj(stock_data)  

        # 计算WR 
        stock_data = calculate_wr(stock_data) 
          
        # 计算RSI  
        stock_data = calculate_rsi(stock_data)  
          
        # 计算布林带  
        stock_data = calculate_bollinger(stock_data)  
          
        # 计算成交量变化百分比  
        stock_data = calculate_vol_change(stock_data) 
        

        # 计算累积打分  
        stock_data = calculate_score(stock_data)  
        
 
        # 回测（这里可以根据需要调整回测天数）    
        stock_data = backtest_strategy(stock_data)    
        #其他任务  
        stock_data['MAXvalue'] = stock_data['total_value'].cummax()  
        stock_data['MINvalue'] = stock_data['total_value'].cummin()   
             
        #不操作的状态
        #stock_data = backtest_strategy_full(stock_data)  
        #stock_data['---MAXvalue'] = stock_data['---total_value'].cummax()  
        #stock_data['---MINvalue'] = stock_data['---total_value'].cummin()
                
		
          
        # 保存每个股票的结果到Excel文件    
        stock_data.to_excel(output_file, index=True)    
        print(f"Data for {stock_name} saved to {output_file}")  
          
        # 将每个股票结果的最后一行添加到汇总DataFrame中  

      
        last_row = stock_data.iloc[-1].to_frame().transpose()  # Convert to DataFrame  
        last_row['StockName'] = stock_name  
        summary_data = pd.concat([summary_data, last_row])
        

    # 计算去除最大最小后的平均值，并忽略错误  
    trimmed_means = summary_data.apply(trimmed_mean)  
          
    # 使用pandas.concat来添加新行，同时重置索引  
    summary_data = pd.concat([summary_data, pd.DataFrame(trimmed_means.rename('Trimmed Means')).T], ignore_index=True)  
    
    try:
        summary_data=mark_stocks(summary_data)
    except f:
        pass
    print(summary_data[['StockName','record']])
    print('\n\n')
    print(summary_data[['ts_code','StockName','score']])  
    print('\n\n')
    print(summary_data[['StockName','record2']])
    print('\n\n')
    print(summary_data[['StockName','total_value','MAXvalue','MINvalue']])  
    
    # 保存汇总结果到Excel文件 
    summary_file = os.path.join(output_dir, '❤❤summary_stock_data.xlsx') 
    summary_data.to_excel(summary_file, index=False)  
    print(f"Summary data saved to {summary_file}")  

# 示例：获取多个股票的数据并保存到Excel    
if __name__ == '__main__':    
	
    stocks_test = {  
         
          "Shinva": "600587.SH",  
          "Yuyue medical": "002223.SZ",  

          "Yaomingkangde": "603259.SH",  
          "Hengrui Pharmaceuticals": "600276.SH",                   
              
          "ZTE": "000063.SZ",  
          "lixun": "002475.SZ",  

          "Midea": "000333.SZ", 
          "Haier": "600690.SH",  

          "Yili": "600887.SH",  
          "PINGAN": "601318.SH",  
        
    } 
    stock1 = {  
 
          "SZZS": "szzs" ,  
    }  #szzs
	
    stocks = {  
          "SZZS": "szzs" , 
          
          "Shinva": "600587.SH",  
          "WeiLi": "603309.SH",  
          "Wandong Medical": "600055.SH",  
          "Yuyue medical": "002223.SZ",  
          "Fosun Pharma": "600196.SH",  
          "Yaomingkangde": "603259.SH",  
          "Yunnan Pharma": "000538.SZ" ,
          "Hengrui Pharmaceuticals": "600276.SH",                   
              
          "Chiese Media": "600373.SH",  

          "ZTE": "000063.SZ",  
          "HKvision": "002415.SZ",  
          "Foxconn": "601138.SH",  
          "lixun": "002475.SZ",  
          'JingDongFang': "000725.SZ",  
          
          "Midea": "000333.SZ", 
          "GREE ":'000651.SZ',  
          "Haier": "600690.SH",  

          "ZiJin": "601899.SH",  
          "jiuAnMedical": "002432.SZ",            
                    
          "Perfect WorLd": "002624.SZ",  
          "Yili": "600887.SH",  
          "HaiTian": "603288.SH", 
          "Guoxing": "002449.SZ",  

          "PINGAN": "601318.SH",  

          "Dasenlin": "603233.SH", 
        
    } 
    stock1 = {  
 
          "SZZS": "szzs" ,  
    }  #szzs
   

    end_date = ''  # 结束日期，留空表示到最新    
    output_dir = './file/'  # 输出目录，可以根据需要修改  
    


    # 获取今天的日期，并格式化为字符串  
    today = datetime.now().strftime('%Y%m%d')  
       
    # 获取一年前的日期（这里假设365天为一年）  
    oneyear_date = datetime.now() - timedelta(days=365)  
    oneyear = oneyear_date.strftime('%Y%m%d')  
      
    # 获取两年前的日期（这里假设730天为两年）  
    twoyear_date = datetime.now() - timedelta(days=730)  
    twoyear = twoyear_date.strftime('%Y%m%d')  
    # 获取3年前的日期（  
    threeyear_date = datetime.now() - timedelta(days=1097)  
    threeyear = threeyear_date.strftime('%Y%m%d')         
     
    fiveyear_date = datetime.now() - timedelta(days=1825)  
    fiveyear = fiveyear_date.strftime('%Y%m%d')  
    tenyear_date = datetime.now() - timedelta(days=3650)  
    tenyear = tenyear_date.strftime('%Y%m%d')  
    if m=='3':
        currentmode=1
        print("Now is Current Mode.")
        m=input("\nPlease input the Code:")

    if m=="":
        currentmode=1
        m='1'
        print("\ndefault:Current Mode & Many codes")   
        stocksx=stocks 
    
    if m=='1':
       stocksx=stocks 
    if m=='5':
       stocksx=stocks_test 
       
    elif m=='2':
        stocksx=stock1   
    elif m=='4':
        dfm=[]
        for stock_name, stock_code in stocks.items(): 
            if stock_code=='szzs':
                stock_code='000001'
            
            stock_code=stock_code.replace('.SZ','')
            stock_code=stock_code.replace('.SH','')   
      
            dfnow = ts.get_realtime_quotes([stock_code])[["code","date","open","high","low","price","pre_close","name","bid","volume","amount"]]
            dfnow['name']=stock_name

            dfnow['pct']=round((dfnow['price'].astype(float)-dfnow['pre_close'].astype(float))/dfnow['pre_close'].astype(float)*100,2)
            dfs=dfnow[['name',"price",'pct']]
            
        
            dfm.append(dfs)
        print(pd.concat(dfm))
            
        
        
    else:
        if m[0]=="6":
            stocksx =  {"❤input":m+'.SH', }  
        if m[0]=="0":
            stocksx =  {"❤input":m+'.SZ', }               
        
    yy=input("\nYears（1/2/3/5/10):")
    if yy=='' or yy=='1':
       print("\ndefault:1 Year")
       start_date= oneyear
    elif  yy=='2':   
       start_date= twoyear 
    elif  yy=='3':   
       start_date= threeyear 
    elif  yy=='5':   
       start_date= fiveyear 
    elif  yy=='10':   
       start_date= tenyear 
    else:
       print("\ndefault:1 Year")
       start_date= oneyear 
    
    main(stocksx, start_date, end_date)

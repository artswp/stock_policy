
import tushare as ts

# 获取当天交易数据

today_all = ts.get_today_all()

'''
code：代码
name:名称
changepercent:涨跌幅
trade:现价
open:开盘价
high:最高价
low:最低价
settlement:昨日收盘价
volume:成交量
turnoverratio:换手率
amount:成交金额
per:市盈率
pb:市净率
mktcap:总市值pyt
nmc:流通市值
'''


#从今日数据按策略选出
"""
>昨天高价：max(昨开，昨收)
1.今开>昨max
2.今收>昨max

"""
start_today='2020-05-16'
end_last='2020-06-16'
for index in today_all.index:
	#filter some not happen
	#     if today_all['changepercent'][index] < 2.0 or today_all['settlement'][index] ==0 or today_all['changepercent'][index] > 8.0:
	#         today_all.drop([index],inplace=True)
	#         continue  

	#temp data
	settlement = today_all['settlement'][index] 
	open       = today_all['open'][index]
	trade      = today_all['trade'][index]
	code       = today_all['code'][index]
	name       = today_all['name'][index]
	if code is None or name is None or len(name)<=0:
		continue
	if code[0]=='3' or name[0]=='*' or name[0]=='S':
		continue #过滤掉创业板和带*的
	#价格小于30.00	
	if trade > 30.0:
		continue
	
	try:
		#下载最近20天的股价
		hist=ts.get_hist_data(code,start=start_today,end=end_last)
	except :
		continue

	
	'''
	date：日期
	open：开盘价
	high：最高价
	close：收盘价
	low：最低价
	volume：成交量
	price_change：价格变动
	p_change：涨跌幅
	ma5：5日均价
	ma10：10日均价
	ma20:20日均价
	v_ma5:5日均量
	v_ma10:10日均量
	v_ma20:20日均量
	turnover:换手率[注：指数无此项]
	'''
	#判断是否水上漂
	#判断第一天涨幅是否大于8%则舍弃
	if hist is None or hist.empty :
		continue
	if hist['p_change'][0] < 8.0:
		 #循环判断前5个的收盘价是否都大于5日线，连续4日则列出来 
		if hist['close'][0]>hist['ma5'][0] \
			and hist['close'][1]>hist['ma5'][1] \
			and hist['close'][2]>hist['ma5'][2] \
			and hist['high'][0]>hist['high'][1]>hist['high'][2]\
			and hist['low'][0]>hist['low'][1]>hist['low'][2]:
			print(today_all['code'][index],",",today_all['name'][index],"三阳开泰,节节高*****")
			continue
	if hist['p_change'][1]< -2.0 and hist['p_change'][0] > 0: #昨日必须是跌-2%一下,今日必须是涨,#低开高走，
		if hist['open'][0] < hist['close'][1] and hist['close'][0] > hist['close'][1]	\
			and ((hist['close'][0] - hist['open'][0])/hist['close'][0] *100) >5.0:
				print(today_all['code'][index],",",today_all['name'][index],"阳吞阴*****")
				continue	



	#jump space
	open_percent= (open - settlement)/settlement *100
	if open > settlement and trade > settlement and open_percent > 2.0 and hsit[p_change][1] <8.0:
		print(today_all['code'][index],",",today_all['name'][index],"跳空选股")
		continue


	#goog line

	anti = today_all['high'][index] - today_all['trade'][index]
	body = today_all['trade'][index] - today_all['open'][index]
	if body==0:
		body=1
	# print("today_all['changepercent'][index]:",today_all['changepercent'][index])
	# print("today_all['changepercent'][low]:",today_all['low'][index])
	if today_all['changepercent'][index] > 5.0 and today_all['changepercent'][index] < 9.0 and today_all['open'][index] - today_all['low'][index] == 0 and anti/body >1/3:
		print(today_all['code'][index],",",today_all['name'][index],"捉腰选股")
		continue
	# if dropline:
	#     today_all.drop([index],inplace=True)
# print(today_all)




'''
跳空：
最小跳空2%，收涨8%内
1.周线跳空:
1.1周线跳空，比如周一产生跳空
1.2周线跳空5周线，前1~2天温和放量
2.日线跳空，周线连续
2.1日线跳空，不产生周线跳空，
2.1跳空日线5日线,前1~2天温和放量极好，突然放量需要观察1~2天
2.1跳空日线20日线,相当于跳空周线
'''

'''
捉腰
今开始最低价
涨幅>6%
上影线小于涨幅1/3

前1~2天温和放量，当天倍量

'''

'''
4~5连阳
连续4日股价范围在5日线上
'''

'''
吞噬

'''

'''
特点：
攻击线：
1.1分为周攻击、日攻击
1.2攻击前温和放量
1.3攻击时放量
1.4攻击后稳住攻击线
1.5攻击方式为跳空、大阳线、吞噬
活力线
1.1
'''

'''
1.三阳开泰
2.
'''
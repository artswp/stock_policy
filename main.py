
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

for index in today_all.index:
    dropline=False
    if today_all['open'][index] > today_all['settlement'][index] and today_all['trade'][index] > today_all['settlement'][index]:
        dropline=False
    else:
        dropline=True
    
    if(dropline):
        anti = today_all['high'][index] - today_all['trade'][index]
        body = today_all['trade'][index] - today_all['open'][index]
        if today_all['changepercent'][index] > 5.0 and today_all['changepercent'][index] < 9.0 and today_all['open'][index] - today_all['low'][index] == 0 and anti/body >1/3:
            dropline=False
        else:
            dropline=True
    if dropline:
        today_all.drop([index],inplace=True)
print(today_all)

'''
捉腰
今开始最低价
涨幅>6%
上影线小于涨幅1/3

'''
#````
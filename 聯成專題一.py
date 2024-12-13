import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager

#解析度
dpi_value=128

#開啟檔案
data_name = 'economy.json'

data=open(data_name,'r',encoding='utf-8')

data_read=data.read()

data_json=eval(data_read)
# 使用 pandas 讀取 JSON 數據並轉換成 DataFrame
data_dataframe = pd.json_normalize(data_json)

#因最後一行都是預估值故刪除
data_dataframe.drop(data_dataframe.index[-1],inplace=True)

#每五年取一次資料
data_dataframe_5year = data_dataframe.iloc[-1::-5][::-1]

#取GDP資料
data_dataframe_GDP = data_dataframe[["產業結構（按各產業GDP比重）-農業","產業結構（按各產業GDP比重）-工業","產業結構（按各產業GDP比重）-服務業"]]


Industry_and_services_grow_rate=[0]#工業及服務業平均月薪增長率
manufacturing_grow_rate=[0]#製造業平均月薪增長率

#計算增長率
keep=None
for i in data_dataframe_5year["工業及服務業平均月薪資（元）"].astype(int):
    if keep!=None:
        Industry_and_services_grow_rate.append(round((i-keep)*100/keep, 2))
    keep=i

    
keep=None
for i in data_dataframe_5year["製造業平均月薪資（元）"].astype(int):
    if keep!=None:
        manufacturing_grow_rate.append(round((i-keep)*100/keep, 2))
    keep=i


#尋找字體名稱
for font in font_manager.fontManager.ttflist:
    if font.fname.split('\\')[-1]=='msyh.ttc':
        fname=font.name

#設定字體
plt.rcParams['font.sans-serif'] = [fname]

#=======================圖片1==========================================================================================================

#設定標題
plt.title("台灣年度國內各項經濟指標",fontsize=24)

#繪製折線圖
plt.errorbar(data_dataframe['年度'].astype(int), data_dataframe['經濟成長率'].astype(float),  label='經濟成長率')

plt.errorbar(data_dataframe['年度'].astype(int), data_dataframe['失業率（百分比）'].astype(float),   label='失業率')

plt.errorbar(data_dataframe['年度'].astype(int), data_dataframe['儲蓄率'].astype(float),label='儲蓄率')

# 設定軸標籤
plt.xlabel('年份',fontsize=18)
plt.ylabel('比\n率\n(%)',rotation=0,labelpad=10,fontsize=16)

#設定軸範圍
plt.ylim(-20,45)
plt.xlim(1993,2025)

#顯示y軸網格線
plt.grid(axis='y')

#設定圖例
plt.legend(loc='lower right')

#保存圖片,bbox_inches = 'tight'解決圖片保存不完整問題
plt.savefig("api1.png", dpi=dpi_value,bbox_inches = 'tight')

#=======================圖片2==========================================================================================================

species = data_dataframe_5year['年度'].astype(int)
penguin_means = {
    '工業及服務業平均月薪': data_dataframe_5year['工業及服務業平均月薪資（元）'].astype(int),
    '製造業平均月薪': data_dataframe_5year['製造業平均月薪資（元）'].astype(int)
}

#位置參數
width = 1.25  
multiplier = 0

#創造圖片
fig, ax = plt.subplots(layout='constrained')

#繪製長條圖
for attribute, measurement in penguin_means.items():
    offset = width * multiplier
    rects = ax.bar(species+offset-0.5,measurement, width, label=attribute)
    multiplier += 1

# 設定軸標籤
ax.set_ylabel('平\n均\n月\n薪\n(元)', rotation=0,labelpad=10,fontsize=11)
ax.set_xlabel('年份',fontsize=14)
ax.set_title('工業及服務業與製造業薪資比較',fontsize=18,)

# 設定軸刻度
ax.set_xticks(species,species)
ax.set_ylim(0, 105000)

#設定圖例
ax.legend(loc='upper left')

#繪製折線圖
ax2=plt.twinx()
ax2.set_ylim(-75,55)
ax2.set_ylabel('平\n均\n月\n薪\n增\n長\n率\n(%)', rotation=0,labelpad=10,verticalalignment='baseline',fontsize=11)
plt.plot(species,Industry_and_services_grow_rate,marker='.',label="工業及服務業平均月薪增長率")
for a,b in zip(species,manufacturing_grow_rate):
    plt.text(a,b+3,b,ha='center',va='bottom',color='darkorange')
plt.plot(species,manufacturing_grow_rate,marker='.',label="製造業平均月薪增長率")
for a,b in zip(species,Industry_and_services_grow_rate):
    plt.text(a,b-3,b,ha='center',va='top',color='dodgerblue')
plt.legend()
plt.savefig("api2.png", dpi=dpi_value,bbox_inches = 'tight')

#=======================圖片3==========================================================================================================

#繪製第一張圓餅圖
fig3, ax3 = plt.subplots(1,2,figsize=(8, 3))

ax3[0].set_title("2002-2012產業GDP比重平均")

data = [data_dataframe["產業結構（按各產業GDP比重）-農業"].iloc[7:18].astype(float).mean(),
        data_dataframe["產業結構（按各產業GDP比重）-工業"].iloc[7:18].astype(float).mean(),
        data_dataframe["產業結構（按各產業GDP比重）-服務業"].iloc[7:18].astype(float).mean()]
ingredients = ["農業","工業","服務業"]
colors = ['limegreen', 'orange','skyblue']

#繪製圓餅圖
wedges, texts, autotexts = ax3[0].pie(data, autopct=lambda pct:f"{pct:.1f}%",
                                  colors=colors)

ax3[0].legend(wedges, ingredients,
          title="產業名稱",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

#設定圓餅圖內字體
plt.setp(autotexts, size=10, weight="bold")

#繪製第二張圓餅圖
data = [data_dataframe["產業結構（按各產業GDP比重）-農業"].iloc[18:].astype(float).mean(),
        data_dataframe["產業結構（按各產業GDP比重）-工業"].iloc[18:].astype(float).mean(),
        data_dataframe["產業結構（按各產業GDP比重）-服務業"].iloc[18:].astype(float).mean()]

wedges, texts, autotexts = ax3[1].pie(data, autopct=lambda pct:f"{pct:.1f}%",
                                  colors=colors)

ax3[1].legend(wedges, ingredients,
          title="產業名稱",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=10, weight="bold")

ax3[1].set_title("2013-2022產業GDP比重平均")
plt.savefig("api3.png", dpi=dpi_value)

#=======================圖片4==========================================================================================================

plt.figure(figsize=(9,6))

plt.title("產業結構（按各產業GDP比重）",fontsize=24,y=1)



plt.errorbar(data_dataframe['年度'].iloc[7:].astype(int), data_dataframe["產業結構（按各產業GDP比重）-服務業"].iloc[7:].astype(float),linewidth=3,marker='o',markevery=5,markersize=8,markerfacecolor='white',label='服務業')

plt.errorbar(data_dataframe['年度'].iloc[7:].astype(int), data_dataframe["產業結構（按各產業GDP比重）-工業"].iloc[7:].astype(float),linewidth=3,marker='o',markevery=5,markersize=8,markerfacecolor='white',   label='工業')

plt.errorbar(data_dataframe['年度'].iloc[7:].astype(int), data_dataframe["產業結構（按各產業GDP比重）-農業"].iloc[7:].astype(float),linewidth=3,marker='o',markevery=5,markersize=8,markerfacecolor='white',  label='農業')

for a,b in zip(data_dataframe['年度'].iloc[7::5].astype(int),data_dataframe["產業結構（按各產業GDP比重）-服務業"].iloc[7::5].astype(float)):
    plt.text(a,b+2,b,ha='center',va='bottom',color='dodgerblue',fontsize=16)
for a,b in zip(data_dataframe['年度'].iloc[7::5].astype(int),data_dataframe["產業結構（按各產業GDP比重）-工業"].iloc[7::5].astype(float)):
    plt.text(a,b+2,b,ha='center',va='bottom',color='darkorange',fontsize=16)
for a,b in zip(data_dataframe['年度'].iloc[7::5].astype(int),data_dataframe["產業結構（按各產業GDP比重）-農業"].iloc[7::5].astype(float)):
    plt.text(a,b+2,b,ha='center',va='bottom',color='g',fontsize=16)
plt.legend()
plt.xlabel('年份',fontsize=20)
plt.ylabel('比\n重\n(%)',rotation=0,labelpad=10,fontsize=16)
plt.ylim(0,100)

plt.xlim(2000,2025)
plt.legend(prop={'size':18})



plt.savefig("api4.png", dpi=dpi_value)
plt.show()
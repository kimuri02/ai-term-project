import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


# import matplotlib.pyplot as plt

# df = pd.read_csv('data/서울시 우리마을가게 상권분석서비스(상권배후지-소득소비).csv', encoding='CP949')
df = pd.read_csv('raw_data/income_consumption.csv', encoding='CP949')

code = df.iloc[1:, 4].tolist()
# print(code)
income = df.iloc[1:, 6].tolist()
consumption = df.iloc[1:, 8].tolist()

income_dic = {code[0]:income[0]}
consumption_dic = {code[0]:consumption[0]}
prev_code = []

for i in range(1,len(code)):    
    if code[i] in income_dic.keys():
        income_dic[code[i]] += income[i]
        consumption_dic[code[i]] += consumption[i]
    else:   
        income_dic[code[i]] = income[i]
        consumption_dic[code[i]] = consumption[i]

fig, axs = plt.subplots(2)
fig.subplots_adjust(hspace=1)
axs[0].set_title('average income')
axs[0].bar(income_dic.keys(), income_dic.values())


axs[1].set_title('average consumption')
axs[1].bar(income_dic.keys(), consumption_dic.values())

plt.show()
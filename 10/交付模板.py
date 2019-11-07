import pandas as pd

df1=pd.read_excel('结果9.xlsx')
df2=pd.read_excel('挖槽模板3.xlsx')
index=list(df2['语料'])
#print(df1.head(),df2.head())

a=df1['语料'].isin(index)
b=[]
for i in a:
    if i:
        b.append(False)
    else:
        b.append(True)

f=df1[b]
f['模板']=list(f['语料'])
print(f.head())
ff=pd.concat([df2,f])
ff[['Label','模板','职业','年龄限制','渠道']].reset_index().to_excel('交付模板9.xlsx',index=None)

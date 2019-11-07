import pandas as pd
import numpy as np
df1=pd.read_excel('nlg模板9.xlsx')
df2=pd.read_excel('标注.xlsx')

d={}
for i in range(len(df2)):
    level=df2['语气等级'][i]
    if not np.isnan(level):
        d[df2['模板'][i]]=int(level)

degree=[]
for i in range(len(df1)):
    label=df1['Label'][i]
    if ('接受' in label) or ('拒绝' in label):
        muban=label=df1['模板'][i]
        if muban in d:
            degree.append(d[muban])
        else:
            degree.append('通用')
    else:
        degree.append('通用')

df1['语气程度']=degree
df1.to_excel('nlg模板(语气)9.xlsx',index=None)


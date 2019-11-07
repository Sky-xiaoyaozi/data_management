import pandas as pd

df1=pd.read_excel('nlg模板(语气)9.xlsx')
df2=pd.read_excel('修改-玉洁.xlsx')

change={}
delete=[]
for i in range(len(df2)):
    key=df2['模板'][i]
    value=df2['模板修改部分'][i]
    if value!='暂时不放入模板中':
        change[key]=value
    else:
        delete.append(key)

count=0
for i in range(len(df1)):
    muban=df1['模板'][i]
    for k in change:
        if muban==k:
            df1['模板'][i]=change[k]
            count+=1
print(delete)
df3=df1[~df1['模板'].isin(delete)]
print(len(df1),len(df3))
index=list(range(1,len(df3)+1))
df3['index']=index

ci_dict=pd.read_excel('词典.xlsx')
writer = pd.ExcelWriter('nlg模板修正10.xlsx')
df3.to_excel(writer, sheet_name='Sheet1',index=None)
ci_dict.to_excel(writer, sheet_name='Sheet2',index=None)
writer.save()
import pandas as pd

df=pd.read_excel('交付模板9.xlsx')

age=[]
for i in range(len(df)):
    x=df['年龄限制'][i]
    if x=='通用':
        age.append('(-,-)')
    elif x=='20-30':
        age.append('(20,30)')
    elif x=='30-40':
        age.append('(30,40)')
    elif x=='40-50':
        age.append('(40,50)')
    elif x=='50以上':
        age.append('(50,-)')
    else:
        print(x)

df['年龄限制']=age
print(df.head())
df.to_excel('nlg模板9.xlsx',index=None)
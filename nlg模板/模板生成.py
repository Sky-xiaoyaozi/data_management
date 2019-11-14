import re
import jieba
import pandas as pd

def create_dict(name='词典3.txt'):
    list_dict=[]
    short_dict = {}
    long_dict={}
    with open(name,'r',encoding='utf-8')as f:
        for line in f:
            row_list=line.strip().split('\t')
            if len(row_list)>3:
                value, type, attr, key =row_list
            else:
                value, type, attr =row_list
                key=''

            if len(key)<=2:
                short_dict[key] = value
            else:
                long_dict[key]=value
            list_dict.append([value,type,attr,key])
    return short_dict,long_dict,list_dict


def create_muban(df,sd,ld):
    short_index = list(sd.keys())
    short_index.sort(key=lambda i: len(i), reverse=True)
    long_index = list(ld.keys())
    long_index.sort(key=lambda i: len(i), reverse=True)
    l = []
    label=[]
    for i in range(len(df)):
        a = df['槽位'][i]
        b = df['子槽位'][i]
        if b=='/':
            b='nan'
        c = df['客户回答类型'][i]
        key = '_'.join([a, b, c])
        value = df['客户话术'][i]
        yuanzhiye = [df['类型'][i],df['年龄限制'][i],df['沟通渠道（电话/微信/通用）'][i]]
        if value == '/':
            f = df['映射槽位'][i]
            g = df['映射子槽位'][i]
            h = df['映射客户回答类型'][i]
            z=df['映射类型'][i]
            dfdf=df[(df['槽位'] == f) & (df['子槽位'] == g) & (df['客户回答类型'] == h)]#& (df['是否是万能句式'] == '否')
            values =dfdf['客户话术']
            yuanzhiyes=[[a,b,c] for a,b,c in zip(dfdf['类型'],dfdf['年龄限制'],dfdf['沟通渠道（电话/微信/通用）'])]

        else:
            values=[value]
            yuanzhiyes=[yuanzhiye]
        #print(values,yuanzhiyes)
        for value,yuanzhiye in zip(values,yuanzhiyes):
            if value == '/':
                f = df['映射槽位'][i]
                g = df['映射子槽位'][i]
                h = df['映射客户回答类型'][i]
                df11=df[(df['槽位'] == f) & (df['子槽位'] == g) & (df['客户话术'] == value)&(df['客户回答类型'] == h) & (df['是否是万能句式'] == '否')]
                f = list(df11['映射槽位'])[0]
                g = list(df11['映射子槽位'])[0]
                h = list(df11['映射客户回答类型'])[0]
                #yuanzhiye = [df['类型'][i],df['年龄限制'][i],df['沟通渠道（电话/微信/通用）'][i]]
                d1f=df[(df['槽位'] == f) & (df['子槽位'] == g) & (df['客户回答类型'] == h) & (df['是否是万能句式'] == '否')]
                new_values =d1f['客户话术']
                for qq in range(len(new_values)):
                    value=new_values.values[qq]
                    y=d1f['沟通渠道（电话/微信/通用）'].values[qq]
                    if value == '你咋有我微信的？':
                        print(qq,y)
                    yuanyuliao=value
                    change = []
                    for k in long_index:
                        if k in value:
                            value = value.replace(k, '{{@' + ld[k] + '}}')
                            change.append(str(ld[k]) + '->' + str(k))
                    for k in short_index:
                        if '{{@' + k not in value:
                            if k in value and ('好吧' not in value) and ('好的' not in value):
                                vs = list(jieba.cut(value))
                                if k in vs:
                                    if k in value:
                                        value = value.replace(k, '{{@' + sd[k] + '}}')
                                        change.append(str(sd[k]) + '->' + str(k))
                    if df['客户话术'][i] != '/':
                        l.append([i + 2, key, df['客户话术'][i], change, value, yuanzhiye[0], yuanzhiye[1],
                                  y])
                    else:
                        l.append([i + 2, key, yuanyuliao, change, value,
                                  yuanzhiye[0],yuanzhiye[1],y])

            else:
                yuanyuliao=value
                change = []
                for k in long_index:
                    if k in value:
                        value = value.replace(k, '{{@' + ld[k] + '}}')
                        change.append(str(ld[k]) + '->' + str(k))
                for k in short_index:
                    if '{{@' + k not in value:
                        if k in value and ('好吧' not in value) and ('好的' not in value):
                            vs = list(jieba.cut(value))
                            if k in vs:
                                if k in value:
                                    value = value.replace(k, '{{@' + sd[k] + '}}')
                                    change.append(str(sd[k]) + '->' + str(k))
                if df['客户话术'][i] != '/':
                    #print(yuanzhiye)
                    l.append(
                        [i + 2, key, df['客户话术'][i], change, value, yuanzhiye[0],yuanzhiye[1],yuanzhiye[2]])
                else:
                    # pass

                    l.append([i + 2, key, yuanyuliao, change, value,
                              yuanzhiye[0],yuanzhiye[1],yuanzhiye[2]])

    return l

if __name__=='__main__':
    df = pd.read_excel('新语料.xlsx')
    df['沟通渠道（电话/微信/通用）'].fillna('通用', inplace=True)
    df['年龄限制'].fillna('通用', inplace=True)
    df.fillna('nan', inplace=True)
    writer = pd.ExcelWriter('结果9.xlsx')

    sd,ld, ll = create_dict()
    l=create_muban(df,sd,ld)
    new_df = pd.DataFrame(l,columns=['Index','Label','语料','识别','模板','职业','年龄限制','渠道'])
    #print(len(new_df))
    df2=new_df.drop_duplicates(subset=['Label','语料','模板','职业','渠道'])#subset=['Index','Label','语料','模板','职业','渠道']
    #print(df2)
    df2.to_excel(writer,index=False)

    df_dict = pd.DataFrame(ll)
    name = df_dict[0].unique()
    for n in name:
        df_dict[df_dict[0] == n].to_excel(writer, sheet_name=n, index=False, header=False)
    writer.save()


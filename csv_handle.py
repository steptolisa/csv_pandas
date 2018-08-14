#coding:utf-8
#python2.7

import pandas as pd

def csv_hd(path_read):

    df_r = pd.read_csv(path_read.decode(encoding = 'utf-8'),index_col=0)
    df_s = df_r
    df_s['ASSET_ID'] = df_s['ASSET_ID'].str.replace('S.+ Equ.+','')
    #获取组合
    porifolios_ = df_s['PORTFOLIO']
    porifolios  = set(porifolios_)
    print(porifolios)
    #获取日期
    dates_ = df_s['DATE']
    dates = set(dates_)
    print(dates)

    #循环日期和组合
    for date in list(dates):
        for porifolio in list(porifolios):
            csh = df_s[(df_s['PORTFOLIO'] == porifolio) & (df_s['DATE'] == date)]            # print(csh)
            #获取CSH_CNY行
            csh_CNY = csh[(csh['ASSET_ID']=='CSH_CNY')]
            row0 = csh_CNY.index
            #选择以C开头的行
            cs = csh[(csh.ASSET_ID.str.startswith('C'))]
            #获取C开头行数
            rows = cs.index
            rows = list(rows)
            #移除CSH_CNY行
            rows.remove(row0)
            #cash -- sum()
            csh_cny = df_s.ix[rows,'HOLDING'].sum()*100 + df_s.ix[row0,'HOLDING']
            #填写cash数据
            df_s.ix[row0, 'HOLDING'] = csh_cny
            #删除行
            df_s = df_s.drop(rows)
    print len(df_s)
#     df_s = df_s.sort_values(by=['PORTFOLIO','DATE','ASSET_ID'])
    df_s.HOLDING = df_s.HOLDING.astype(int)
    df_s.index = range(len(df_s))
    return df_s



path = r'G:\工作文档/A股组合持仓分账户汇总-20180102-20180731_update.csv'


def csv_apart(path_r):
    #读取csv时日期列解析
    df_r = pd.read_csv(path_r.decode(encoding='utf-8'), index_col=0,parse_dates=['L_DATE'])
    df_s = df_r
    #组合数
    porifolios_ = df_s['PORTFOLIO']
    porifolios = set(porifolios_)
    csv_list = []
    #循环组合
    for porifolio in list(porifolios):
        # 挑选同一组合数据
        pori = df_s[(df_s['PORTFOLIO'] == porifolio)]
        # 转换ASSET_ID类型以便可以 '+ str'
        pori.ASSET_ID = pori.ASSET_ID.astype(str)
        # 添加后缀‘-CN'’
        pori.ASSET_ID = pori.ASSET_ID + '-CN'
        #替换空字符串
        pori.ASSET_ID = pori.ASSET_ID.str.replace(' ','')
        #L_DATE(日期)转换
        # pori.L_DATE = pd.to_datetime(pori.L_DATE)
        #更改L_DATE类型
        pori.L_DATE = pori.L_DATE.astype(str)
        #日期列替换'-'
        pori.L_DATE = pori.L_DATE.str.replace('-','')
        #list。append
        csv_list.append(pori)

    #返回各组合csv的列表list
    return csv_list

csv_list = csv_apart(path)

print(csv_list)
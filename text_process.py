# -*- coding: utf-8 -*-
"""
Created on Wed May  2 10:40:32 2018

@author: bin
"""
import pandas as pd
from chinese_province_city_area_mapper.transformer import CPCATransformer
from chinese_province_city_area_mapper import myumap
from street_mapping import mymap
#########地址信息提取#########
def address_extract(data_raw):
    
    data=data_raw.copy()
    cpca = CPCATransformer(myumap.umap)
    nr = data['受理内容'].str.findall(r'(?:^|\n)([^【^】].+)')
    quxian = data['受理内容'].str.findall(r'【区/县】([^【^】^\r^\n]+)')
    luming = data['受理内容'].str.findall(r'【路名】([^【^】^\r^\n]+)')
    data['区/县'] = quxian.str.get(0)
    data['路名']= luming.str.get(0)
    data['受理正文内容']=nr.str.join('')
    data['受理正文内容'] = data['受理正文内容'].str.strip()
    addr_df = cpca.transform(data["受理正文内容"]).reindex(columns = ['省','市','区'])
    data = pd.concat([data, addr_df], axis=1)
    data['街道'] = data.apply(mymap,axis=1)
    processed = data.apply(mix_addr,axis = 1)
    processed.drop(['区/县','路名','受理正文内容'],axis=1,inplace=True)
    return processed

def mix_addr(df):
    import re
    rigion_sub = ['区', '县', '市', '', '域', '岛', '旗']
    cpca = CPCATransformer(myumap.umap)
    for sub in rigion_sub:
        quxian = str(df['区/县']) + sub
        addr_all = cpca.transform(pd.Series(quxian))
        if addr_all['区'].iloc[0]:
            break
    lum = re.compile(r'^[\u4e00-\u9fa5].*')
    addr_all = addr_all.iloc[0]
    if not df['区'] and not df['市']:
        df['区'] = addr_all['区']
        df['市'] = addr_all['市']
        df['省'] = addr_all['省']
    elif not df['区'] and df['市']:
        df['区'] = addr_all['区']
    if not df['街道']:
        if re.match(lum,str(df['路名'])):
            df['街道'] = df['路名']
    return df
      
#########结构化信息提取#########
def structured_info_extract(data):
    rst = data['受理内容'].str.extractall(r'【(.+?)】([^【^】^\r^\n]*)')
    rst.columns = ['受理项目','内容']
    rst['内容']=rst['内容'].str.strip()
    rst.index = rst.index.droplevel(1)
    result = pd.merge(data,rst,how = 'right',left_index=True,right_index=True)
    return result
    
#########产品信息提取#########
def get_products(content_row, products):
    is_in = []  
    for product in products:  
        if product in content_row:
            is_in.append(product)
    return "|".join(is_in)

def products_extract(data_raw,product_lst):
    data=data_raw.copy()
    data['产品信息']=data['受理内容'].apply(lambda x:get_products(x,product_lst))
    return data
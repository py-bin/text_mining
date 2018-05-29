# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 11:39:13 2018

@author: bin
"""
import re

def mymap(df):
    area = ''
    loc_e = 0
    string = df['受理正文内容']
    near = 12
    rst = ''
    if df['区']:
        area = df['区']
        if string.find(area)>0:
            loc_b = string.find(area)+len(area)
            loc_e = loc_b + near
        else:
            area = df['区'][:-1]
            loc_b = string.find(area)+len(area)
            loc_e = loc_b + near
    elif df['市']:
        area = df['市']   
        if string.find(area)>0:
            loc_b = string.find(area)+len(area)
            loc_e = loc_b + near
        else:
            area = df['市'][:-1]
            loc_b = string.find(area)+len(area)
            loc_e = loc_b + near
    if loc_e:
        loc_string = string[loc_b:loc_e]
        searchObj = re.search(r'.+(?:[街道路村巷乡横厦城区园]|中心|附近)',loc_string)
        if searchObj:
            rst = searchObj.group()
    return rst
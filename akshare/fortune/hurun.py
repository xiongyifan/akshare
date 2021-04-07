# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/4/7 13:04
Desc: 胡润排行榜
http://www.hurun.net/CN/HuList/Index
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup


def hurun_rank(indicator: str = "胡润全球独角兽榜", year: str = "2020") -> pd.DataFrame:
    """
    胡润排行榜
    http://www.hurun.net/CN/HuList/Index?num=3YwKs889SRIm
    :param indicator: choice of {"胡润百富榜", "胡润全球富豪榜", "胡润印度榜", "胡润全球独角兽榜", "胡润Under30s创业领袖榜", "胡润·平安中国好医生榜", "胡润中国500强民营企业", "胡润世界500强", "胡润艺术榜"}
    :type indicator: str
    :param year: 指定年份; {"胡润百富榜": "2019至今", "胡润全球富豪榜": "2015至今", "至尚优品": "2017至今"}
    :type year: str
    :return: 指定 indicator 和 year 的数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.hurun.net/zh-CN/Rank/HsRankDetails?num=Q9TGQF1L"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    url_list = ['https://www.hurun.net' + item['href'] for item in soup.find('div', attrs={'aria-labelledby': 'navbarDropdown'}).find_all('a')]
    name_list = [item.text for item in soup.find('div', attrs={'aria-labelledby': 'navbarDropdown'}).find_all('a')]
    name_url_map = dict(zip(name_list, url_list))
    r = requests.get(name_url_map[indicator])
    soup = BeautifulSoup(r.text, 'lxml')
    code_list = [item['value'].split('=')[1] for item in soup.find(attrs={'id': 'exampleFormControlSelect1'}).find_all('option')]
    year_list = [item.text.split(' ')[0] for item in soup.find(attrs={'id': 'exampleFormControlSelect1'}).find_all('option')]
    year_code_map = dict(zip(year_list, code_list))
    params = {
        'num': year_code_map[year],
        'search': ''
    }
    url = 'https://www.hurun.net/zh-CN/Rank/HsRankDetailsList'
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    if indicator == '胡润百富榜':
        temp_df.columns = [
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '排名',
            '财富',
            '姓名',
            '_',
            '_',
            '企业',
            '_',
            '_',
            '_',
            '行业',
            '_',
            '_',
            '_',
        ]
        temp_df = temp_df[[
            '排名',
            '财富',
            '姓名',
            '企业',
            '行业',
        ]]
    elif indicator == '胡润全球独角兽榜':
        temp_df.columns = [
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '_',
            '排名',
            '财富',
            '姓名',
            '_',
            '_',
            '企业',
            '_',
            '_',
            '_',
            '行业',
            '_',
            '_',
        ]
        temp_df = temp_df[[
            '排名',
            '财富',
            '姓名',
            '企业',
            '行业',
        ]]
    return temp_df


if __name__ == "__main__":
    hurun_rank_df = hurun_rank(indicator="胡润全球独角兽榜", year="2020")
    print(hurun_rank_df)

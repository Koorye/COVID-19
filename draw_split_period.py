# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Date: 2020/6/13
# @Author: Koorye

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = pd.read_csv('data/tiny_differ_timeline_international_daily.csv', index_col=0)
    country_dic = {'Canada': [84, 125],
                   'United Kingdom': [92, 128],
                   'Italy': [65, 118],
                   'Turkey': [76, 108],
                   'US': [88, 130]}

    for country in country_dic:
        x_list = range(country_dic[country][0], country_dic[country][1])
        temp_list = data.loc[country].to_list()
        y_list = []
        for x in x_list:
            y_list.append(temp_list[x])

        print(x_list)
        print(y_list)
        plt.figure(figsize=(10, 6))
        plt.plot(x_list, y_list)
        plt.xlabel('Days')
        plt.ylabel('Tiny Differ')
        plt.title('Tiny Differ in K3 of {}'.format(country))
        plt.savefig('img/tiny_differ_in_k3_of_{}.png'.format(country))

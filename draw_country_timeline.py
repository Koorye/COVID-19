# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Date: 2020/6/11
# @Author: Koorye

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_fitting_poly(x_data, y_data, level):
    array = np.polyfit(x_data, y_data, level)
    poly = np.poly1d(array)
    return poly


if __name__ == '__main__':
    country_list = ['Italy', 'US']
    MAX_LAST_DAYS = 100
    DAYS_STEP = 20
    confirmed_increased_data = pd.read_csv('data/confirmed_timeline_international_increased_daily.csv',
                                           header=None, index_col=0)
    recovered_increased_data = pd.read_csv('data/recovered_timeline_international_increased_daily.csv',
                                           header=None, index_col=0)
    deaths_increased_data = pd.read_csv('data/deaths_timeline_international_increased_daily.csv',
                                        header=None, index_col=0)
    tiny_differ_data = pd.read_csv('data/tiny_differ_timeline_international_daily.csv',
                                   header=None, index_col=0)
    obvious_differ_data = pd.read_csv('data/obvious_differ_timeline_international_daily.csv',
                                      header=None, index_col=0)

    for country in country_list:
        confirmed_increased_list = confirmed_increased_data.loc[country].to_list()
        recovered_increased_list = recovered_increased_data.loc[country].to_list()
        deaths_increased_list = deaths_increased_data.loc[country].to_list()
        tiny_differ_list = tiny_differ_data.loc[country].to_list()
        obvious_differ_list = obvious_differ_data.loc[country].to_list()

        poly = get_fitting_poly(range(len(tiny_differ_list)), tiny_differ_list, 12)
        fitting_list = poly(range(len(tiny_differ_list)))

        for last_index in range(DAYS_STEP, MAX_LAST_DAYS + DAYS_STEP, DAYS_STEP):
            plt.figure(figsize=(10, 6))
            plt.bar(range(len(confirmed_increased_list[-last_index:])), confirmed_increased_list[-last_index:],
                    color='yellow', label='Confirmed Daily')
            plt.bar(range(len(recovered_increased_list[-last_index:])),
                    0 - np.array(recovered_increased_list[-last_index:]),
                    color='limegreen', label='Recovered Daily')
            plt.bar(range(len(deaths_increased_list[-last_index:])),
                    0 - np.array(deaths_increased_list[-last_index:]),
                    color='red', label='Deaths Daily')

            plt.plot(tiny_differ_list[-last_index:], color='dodgerblue', linewidth='1.5', label='Tiny Differ')
            plt.plot(obvious_differ_list[-last_index:], color='coral', linewidth='1.5', label='Obvious Differ')
            plt.plot(fitting_list[-last_index:], color='deeppink', linewidth='3', label='Fitting Differ')

            plt.legend(loc='best')
            plt.title('{} Timeline Recent {} Days'.format(country, last_index))
            plt.savefig('img/{}_timeline_recent_{}_days.png'.format(country, last_index))

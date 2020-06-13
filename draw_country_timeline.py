# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Date: 2020/6/11
# @Author: Koorye

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime


def get_fitting_poly(poly_x_data, poly_y_data, level):
    array = np.polyfit(poly_x_data, poly_y_data, level)
    fitting_poly = np.poly1d(array)
    return fitting_poly


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
        diff_poly = np.polyder(poly)
        diff2_poly = np.polyder(diff_poly)
        date_data = []
        date = datetime.datetime.strptime('2020-1-24', '%Y-%m-%d')
        for i in range(130):
            date_data.append(date)
            date = date + datetime.timedelta(days=1)

        x_data = np.array(range(130))
        y0_data = poly(x_data)
        y1_data = diff_poly(x_data)
        y2_data = diff2_poly(x_data)
        break_point_list = np.array([114, 89, 44, 35, 23])
        second_diff_break_point_list = diff2_poly(break_point_list)

        plt.figure(figsize=(10, 6))
        # plt.plot(x_data, y0_data, label='primitive')
        plt.plot(x_data, y1_data, label='first derivative')
        plt.plot(date_data, y2_data, label='second derivative')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.xticks(rotation=30)
        plt.legend()
        plt.savefig('img/poly_of_{}.png'.format(country))

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

# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Date: 2020/6/11
# @Author: Koorye

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def cal_fitting_goodness(x_list, data_list, fitting_poly):
    """ Calculating fitting goodness, return a list of
    fitting ploy, relevance, regression, residual, total sum of squares. """
    y_prd = fitting_poly(x_list)

    # regression sum of squares
    regression = sum((y_prd - np.mean(data_list)) ** 2)

    # residual sum of squares
    residual = sum((data_list - y_prd) ** 2)

    # total sum of squares
    total = sum((data_list - np.mean(data_list)) ** 2)
    relevance = 1 - residual / total
    return [fitting_poly, relevance, regression, residual, total]


def plot_poly_fitting(data_list, p_level_start, p_level_end, p_level_step, plot_country):
    """ Draw poly fitting plot from data. """
    plt.figure(figsize=(10, 6))
    data_frame = pd.DataFrame(columns=['Fitting Poly', 'Relevance', 'Regression Sum of Squares',
                                       'Residual Sum of Squares', 'Total Sum of Squares'])

    for p_level in range(p_level_start, p_level_end + 1):
        x_list = np.array(range(len(data_list)))
        array = np.polyfit(x_list, data_list, p_level)
        poly = np.poly1d(array)
        y_list = poly(x_list)

        data_frame.loc[p_level] = cal_fitting_goodness(x_list, data_list, poly)

        plt.plot(x_list, y_list, label=str(p_level) + ' - term fitting')
        plt.xlabel('Days')
        plt.ylabel('People')
        plt.title('Poly Fitting Analyze of Tiny Inflection Point in {}'.format(plot_country))
        plt.legend(loc='best')

        if p_level % p_level_step == 0:
            plt.plot(tiny_differ_list, label='tiny inflection point')
            plt.savefig('img/poly_fitting_analyze_of_tiny_inflection_point_in{}_from_{}_to_{}.png'
                        .format(plot_country, p_level - p_level_step + 1, p_level))
            plt.clf()

    data_frame.to_csv('data/fitting_goodness_of_tiny_inflection_point_in_{}.csv'.format(plot_country))
    plt.clf()
    plt.figure(figsize=(10, 6))
    plt.plot(range(level_start, level_end + 1), data_frame['Relevance'].to_list())
    plt.xlabel('P-level')
    plt.ylabel('R-square')
    plt.title('R-square with P-level')
    plt.savefig('img/R_square_with_poly_of_{}.png'.format(country))


if __name__ == '__main__':
    country_list = ['Italy', 'US']
    level_start = 6
    level_end = 20
    level_step = 5
    tiny_differ_data = pd.read_csv('data/tiny_differ_timeline_international_daily.csv', index_col=0)

    for country in country_list:
        tiny_differ_list = tiny_differ_data.loc[country].to_list()
        plot_poly_fitting(tiny_differ_list, level_start, level_end, level_step, country)

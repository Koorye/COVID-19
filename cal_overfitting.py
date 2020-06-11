# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Date: 2020/6/11
# @Author: Koorye

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def cal_fitting_goodness(x_data, y_data, poly):
    """ Calculating fitting goodness, return a list of
    fitting ploy, relevance, regression, residual, total sum of squares. """
    y_prd = poly(x_data)

    # residual sum of squares
    residual = sum((y_data - y_prd) ** 2)

    # total sum of squares
    total = sum((y_data - np.mean(y_data)) ** 2)
    relevance = 1 - residual / total
    return relevance


def get_fitting_poly(x_data, y_data, poly_level):
    """ Get fitting poly from x_data and y_data. """
    array = np.polyfit(x_data, y_data, poly_level)
    poly = np.poly1d(array)
    return poly


def draw_over_fitting_plot(fitting_list, p_level_start, plot_country):
    """ Draw several attempts of calculating over fitting rate. """
    plt.figure(figsize=(10, 6))

    mean_fitting_list = [0 for _ in range(len(fitting_list[0]))]

    for col in range(len(fitting_list[0])):
        for row in range(len(fitting_list)):
            mean_fitting_list[col] = mean_fitting_list[col] + fitting_list[row][col]
    mean_fitting_list = np.array(mean_fitting_list)
    mean_fitting_list = mean_fitting_list / len(fitting_list)

    for member in fitting_list:
        x_data = np.array(range(len(member)))
        x_data = x_data + p_level_start
        plt.plot(x_data, member)

    x_data = np.array(range(len(mean_fitting_list)))
    x_data = x_data + p_level_start
    plt.plot(x_data, mean_fitting_list, linewidth=5, label='Mean')
    plt.xlabel('P-level')
    plt.ylabel('Over Fitting Rate')
    plt.legend()
    plt.title('Over Fitting Rate with P-level')
    plt.savefig('img/over_fitting_rate_with_p_level_of_{}.png'.format(plot_country))
    print('Minimal Over Fitting Level: ', np.argmin(mean_fitting_list) + start_level)


if __name__ == '__main__':
    start_level = 6
    end_level = 20
    circle_time = 20
    country_list = ['Italy', 'US']

    for country in country_list:
        tiny_differ_data = pd.read_csv('data/tiny_differ_timeline_international_daily.csv', header=None, index_col=0)
        data_list = tiny_differ_data.loc[country].to_list()
        x_list = range(len(data_list))

        over_fitting_list = []
        step = 0
        while step < circle_time:
            temp_list = []

            x_train_list = random.sample(x_list, int(len(x_list) * 0.8))
            x_test_list = list(set(x_list) - set(x_train_list))

            y_train_list, y_test_list = [], []
            for index in x_train_list:
                y_train_list.append(data_list[index])
            for index in x_test_list:
                y_test_list.append(data_list[index])

            x_train_list = np.array(x_train_list)
            x_test_list = np.array(x_test_list)
            y_train_list = np.array(y_train_list)
            y_test_list = np.array(y_test_list)

            for level in range(start_level, end_level + 1):
                fitting_poly = get_fitting_poly(x_train_list, y_train_list, level)
                r_square_train = cal_fitting_goodness(x_train_list, y_train_list, fitting_poly)
                r_square_test = cal_fitting_goodness(x_test_list, y_test_list, fitting_poly)
                temp_list.append((1 - r_square_test) / r_square_train)
            if max(temp_list) < 1.5:
                over_fitting_list.append(temp_list)
                step += 1

        draw_over_fitting_plot(over_fitting_list, start_level, country)

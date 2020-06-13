# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Date: 2020/6/12
# @Author: Koorye

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.signal
import csv


def spilt_train_and_test_sets(fitting_data):
    train_x_list = random.sample(range(len(fitting_data)), int(len(fitting_data) * 0.8))
    test_x_list = list(set(range(len(fitting_data))) - set(train_x_list))

    train_x_list.sort()
    test_x_list.sort()

    train_y_list, test_y_list = [], []
    for data in train_x_list:
        train_y_list.append(fitting_data[data])
    for data in test_x_list:
        test_y_list.append(fitting_data[data])

    return np.array(train_x_list), np.array(train_y_list), np.array(test_x_list), np.array(test_y_list)


def get_main_country(global_data_path, first_index, last_index):
    """ Select main country from first index to last index. """
    data = pd.read_csv(global_data_path, header=None)
    data.sort_values(132, ascending=False, inplace=True)
    data.reset_index(drop=True, inplace=True)

    main_country_list = []
    for index, row in data.iterrows():
        if index >= first_index:
            main_country_list.append(row[0])
        if index > last_index:
            return main_country_list


def get_fitting_poly(poly_x_data, poly_y_data, level):
    array = np.polyfit(poly_x_data, poly_y_data, level)
    fitting_poly = np.poly1d(array)
    return fitting_poly


def cal_fitting_goodness(x_data, y_data, fitting_poly):
    """ Calculating fitting goodness, return a list of
    fitting ploy, relevance, regression, residual, total sum of squares. """
    y_prd = fitting_poly(x_data)
    residual = sum((y_data - y_prd) ** 2)
    total = sum((y_data - np.mean(y_data)) ** 2)
    relevance = 1 - residual / total
    return relevance


def cal_over_fitting_rate(train_x_data, train_y_data, test_x_data, test_y_data, fitting_poly):
    train_r_square = cal_fitting_goodness(train_x_data, train_y_data, fitting_poly)
    test_r_square = cal_fitting_goodness(test_x_data, test_y_data, fitting_poly)
    return (1 - test_r_square) / train_r_square


def cal_mean_data(static_data):
    mean_data = np.array([0 for _ in range(len(static_data[0]))])
    for col in range(len(static_data[0])):
        for row in range(len(static_data)):
            mean_data[col] += static_data[row][col]

    return mean_data / len(static_data)


def get_best_fitting_poly(poly_data, fitting_country, p_start_level, p_last_level, fitting_time):
    """ Choose to best fitting poly to split periods of country. """
    over_fitting_rate_list = []
    current_time = 0
    while current_time < fitting_time:
        train_x_list, train_y_list, test_x_list, test_y_list = spilt_train_and_test_sets(poly_data)

        temp_list = []
        for level in range(p_start_level, p_last_level + 1):
            fitting_poly = get_fitting_poly(train_x_list, train_y_list, level)
            temp_list.append(cal_over_fitting_rate(train_x_list, train_y_list, test_x_list, test_y_list, fitting_poly))
        if max(temp_list) < 3:
            over_fitting_rate_list.append(temp_list)
            current_time += 1

    plt.clf()
    plt.figure(figsize=(10, 6))
    for rate in over_fitting_rate_list:
        plt.plot(range(p_start_level, p_last_level + 1), rate)

    mean_data = cal_mean_data(over_fitting_rate_list)
    plt.plot(range(p_start_level, p_last_level + 1), mean_data, linewidth=5, label='mean')

    plt.xlabel('P-level')
    plt.ylabel('Over Fitting Rate')
    plt.title('Over Fitting Rate with P-level of {}'.format(fitting_country))
    plt.legend()
    plt.savefig('img/over_fitting_rate_with_p_level_of_{}.png'.format(fitting_country))

    best_fitting_poly_index = np.argmin(mean_data) + p_start_level
    return get_fitting_poly(range(len(poly_data)), poly_data, best_fitting_poly_index)


def get_split_point(fitting_poly, start_day, end_day):
    day_data = []
    for day in range(start_day, end_day):
        day_data.append(fitting_poly(day))
    day_data = np.array(day_data)

    max_value_list = day_data[scipy.signal.argrelextrema(day_data, np.greater)]
    min_value_list = day_data[scipy.signal.argrelextrema(day_data, np.less)]

    day_data = list(day_data)

    if any(max_value_list) and any(min_value_list):
        return day_data.index(min_value_list[0]) + start_day, \
               day_data.index(max_value_list[len(max_value_list) - 1]) + start_day
    else:
        return None, None


def draw_split_plot(fitting_poly, fitting_country, start_day, end_day, split_point_list):
    day_list = np.array(range(start_day, end_day))
    fitting_list = fitting_poly(day_list)

    plt.clf()
    plt.figure(figsize=(10, 6))
    plt.plot(day_list, fitting_list)
    for point in split_point_list:
        plt.scatter(point, fitting_poly(point), color='red')

    plt.xlabel('Days')
    plt.ylabel('Tiny Differ')
    plt.title('Tiny Differ with Days of {}'.format(fitting_country))
    plt.savefig('img/tiny_differ_with_days_of_{}.png'.format(fitting_country))


if __name__ == '__main__':
    # country_list = get_main_country('data/confirmed_timeline_international.csv', 0, 19)
    country_list = ['US']
    tiny_differ_data = pd.read_csv('data/tiny_differ_timeline_international_daily.csv', index_col=0)
    my_start_day = 30
    my_end_day = 130

    file = open('data/split_day_international_{}_to_{}.csv'.format(my_start_day,my_end_day), 'w', newline='')
    writer = csv.writer(file)
    for country in country_list:
        tiny_differ_list = tiny_differ_data.loc[country].to_list()
        poly = get_best_fitting_poly(tiny_differ_list, country, 5, 20, 20)
        k3_to_k4_day, k2_to_k3_day = get_split_point(poly, my_start_day, my_end_day)
        if k3_to_k4_day and k2_to_k3_day:
            draw_split_plot(poly, country, my_start_day, my_end_day, [k2_to_k3_day, k3_to_k4_day])
            writer.writerow([country, k2_to_k3_day, k3_to_k4_day])
    file.close()

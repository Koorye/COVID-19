# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Date: 2020/6/11
# @Author: Koorye

import pandas as pd


def get_increased_data(input_data_frame):
    """ Input totally data frame then output daily data frame. """
    desc_data = input_data_frame.iloc[:, ::-1]
    for index, col in desc_data.iteritems():
        desc_data[index] = desc_data[index] - desc_data[index - 1]
        if index == 2:
            asc_data = desc_data.iloc[:, ::-1]
            return asc_data


def get_differ_data(data_frame1, data_frame2):
    data_frame = data_frame1.copy()
    for index, col in data_frame2.iteritems():
        if index != 0:
            data_frame[index] = data_frame[index] - data_frame2[index]
    return data_frame


def output_data_into_csv(data_frame, csv_path):
    data_frame.to_csv(csv_path, index=False, header=None)


if __name__ == '__main__':
    confirmed_data = pd.read_csv('data/confirmed_timeline_international.csv', header=None)
    recovered_data = pd.read_csv('data/recovered_timeline_international.csv', header=None)
    deaths_data = pd.read_csv('data/deaths_timeline_international.csv', header=None)

    confirmed_increased_data = get_increased_data(confirmed_data)
    recovered_increased_data = get_increased_data(recovered_data)
    deaths_increased_data = get_increased_data(deaths_data)

    tiny_differ_data = get_differ_data(confirmed_increased_data, recovered_increased_data)
    obvious_differ_data = get_differ_data(tiny_differ_data, deaths_increased_data)
    output_data_into_csv(confirmed_increased_data, 'data/confirmed_timeline_international_increased_daily.csv')
    output_data_into_csv(recovered_increased_data, 'data/recovered_timeline_international_increased_daily.csv')
    output_data_into_csv(deaths_increased_data, 'data/deaths_timeline_international_increased_daily.csv')
    output_data_into_csv(tiny_differ_data, 'data/tiny_differ_timeline_international_daily.csv')
    output_data_into_csv(obvious_differ_data, 'data/obvious_differ_timeline_international_daily.csv')

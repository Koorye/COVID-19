# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Date: 2020/6/11
# @Author: Koorye

""" Stating provinces of each country then get total confirmed/recovered/deaths timeline of each country. """

import pandas as pd
import csv


def arrange_map_from_csv(input_csv_path):
    """ Read Global data, merging provinces/states of each country into a map. """
    input_data_frame = pd.read_csv(input_csv_path)
    country_map = {}

    for index, row in input_data_frame.iterrows():
        if row[1] not in country_map:
            country_map[row[1]] = row[4:]
        else:
            for i in range(len(country_map[row[1]]) + 4):
                if i >= 4:
                    country_map[row[1]][i - 4] += row[i]

    return country_map


def output_map_into_csv(country_map, output_csv_path):
    """ Output the map into csv. """
    output_csv = open(output_csv_path, 'w', encoding='utf-8', newline='')
    writer = csv.writer(output_csv)

    for key, value in country_map.items():
        new_row = [key]
        for each in value:
            new_row.append(str(each))
        writer.writerow(new_row)
    output_csv.close()

    data = pd.read_csv(output_csv_path,header=None)
    data.sort_values(0, inplace=True)
    data.to_csv(output_csv_path, index=False, header=None)


if __name__ == '__main__':
    confirmed_map = arrange_map_from_csv(
        'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    recovered_map = arrange_map_from_csv(
        'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    deaths_map = arrange_map_from_csv(
        'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

    output_map_into_csv(confirmed_map, 'data/confirmed_timeline_international.csv')
    output_map_into_csv(recovered_map, 'data/recovered_timeline_international.csv')
    output_map_into_csv(deaths_map, 'data/deaths_timeline_international.csv')

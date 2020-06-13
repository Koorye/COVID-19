# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Date: 2020/6/13
# @Author: Koorye

import numpy as np
import pandas as pd
import tensorflow as tf
import random
import matplotlib.pyplot as plt


def spilt_train_and_test_sets(fitting_data):
    train_x_list = random.sample(range(len(fitting_data)), int(len(fitting_data) * 0.8))
    test_x_list = list(set(range(len(fitting_data))) - set(train_x_list))

    train_x_list.sort()
    test_x_list.sort()

    train_y_list, test_y_list = [], []
    for train_data in train_x_list:
        train_y_list.append(fitting_data[train_data])
    for test_data in test_x_list:
        test_y_list.append(fitting_data[test_data])

    return np.array(train_x_list), np.array(train_y_list), np.array(test_x_list), np.array(test_y_list)


if __name__ == '__main__':
    country_period_dic = {'US': [88, 130]}
    data = pd.read_csv('data/tiny_differ_timeline_international_daily.csv', index_col=0)

    for country in country_period_dic:
        y_data = np.array(data.loc[country].to_list()[country_period_dic[country][0]:country_period_dic[country][1]])
        train_x_data, train_y_data, test_x_data, test_y_data = spilt_train_and_test_sets(y_data)

        train_x_data = np.reshape(train_x_data, (train_x_data.shape[0], 1, 1))
        test_x_data = np.reshape(test_x_data, (test_x_data.shape[0], 1, 1))

        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(128, input_dim=1, return_sequences=True),
            tf.keras.layers.LSTM(128),
            tf.keras.layers.Dense(1, activation='linear')
        ])

        model.compile(optimizer='adam', loss='mse')

        model.fit(train_x_data, train_y_data, epochs=1024,
                  validation_data=(test_x_data, test_y_data),
                  validation_freq=10)

        predict_y_data = model.predict(np.reshape(np.array(range(0, 160)), (np.array(range(0, 160)).shape[0], 1, 1)))
        plt.plot(np.array(range(0, 160)), predict_y_data)
        plt.show()

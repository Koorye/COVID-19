import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd


def get_plot_list(csv_path, first_index, last_index):
    """ Read csv, selecting data from first index to last index. """
    data = pd.read_csv(csv_path, header=None)
    data.sort_values(132, ascending=False, inplace=True)
    data.reset_index(drop=True, inplace=True)

    plot_list = []
    for index, row in data.iterrows():
        if index >= first_index:
            plot_list.append(row[0])
        if index > last_index:
            return plot_list


def plot_timeline_from_csv(csv_path, plot_list, plot_title, plot_path):
    """ Read csv, selecting each row of data in the plot list into plot. """
    data = pd.read_csv(csv_path, header=None)
    plt.figure(figsize=(10, 6))

    for index, row in data.iterrows():
        line = []
        country = ''
        for i in range(len(row)):
            if i == 0:
                country = str(row[0])
            else:
                line.append(int(row[i]))

        if country in plot_list:
            plt.plot(line, label=country)

    plt.title(plot_title)
    plt.xlabel('Days')
    plt.ylabel('Number of People')
    plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    plt.legend(bbox_to_anchor=(1, 1.05))
    plt.subplots_adjust(right=0.8)
    plt.savefig(plot_path)


if __name__ == '__main__':
    top_country_list = get_plot_list('data/confirmed_timeline_international.csv', 0, 19)

    plot_timeline_from_csv('data/confirmed_timeline_international.csv',
                           top_country_list,
                           'Confirmed Timeline International TOP20',
                           'img/confirmed_timeline_international_top20.png')

    plot_timeline_from_csv('data/recovered_timeline_international.csv',
                           top_country_list,
                           'Recovered Timeline International TOP20',
                           'img/recovered_timeline_international_top20.png')

    plot_timeline_from_csv('data/deaths_timeline_international.csv',
                           top_country_list,
                           'Deaths Timeline International TOP20',
                           'img/deaths_timeline_international_top20.png')

    plot_timeline_from_csv('data/confirmed_timeline_international_increased_daily.csv',
                           top_country_list,
                           'Confirmed Timeline International Increased Daily TOP20',
                           'img/confirmed_timeline_international_increased_daily_top20.png')

    plot_timeline_from_csv('data/recovered_timeline_international_increased_daily.csv',
                           top_country_list,
                           'Recovered Timeline International Increased Daily TOP20',
                           'img/recovered_timeline_international_increased_daily_top20.png')

    plot_timeline_from_csv('data/deaths_timeline_international_increased_daily.csv',
                           top_country_list,
                           'Deaths Timeline International Increased Daily TOP20',
                           'img/deaths_timeline_international_increased_daily_top20.png')

    plot_timeline_from_csv('data/tiny_differ_timeline_international_daily.csv',
                           top_country_list,
                           'Tiny Inflection Point Analysis TOP20',
                           'img/tiny_inflection_point_analysis_top20.png')

    plot_timeline_from_csv('data/obvious_differ_timeline_international_daily.csv',
                           top_country_list,
                           'Obvious Inflection Point Analysis TOP20',
                           'img/obvious_inflection_point_analysis_top20.png')

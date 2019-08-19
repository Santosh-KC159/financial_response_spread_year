''' TAQ data tools module.

The functions in the module do small repetitive tasks, that are used along the
whole implementation. These tools improve the way the tasks are standardized
in the modules that use them.

This script requires the following modules:
    * matplotlib
    * numpy
    * pandas

The module contains the following functions:
    * taq_save_data - saves computed data.
    * taq_save_plot - saves figures.
    * taq_function_header_print_data - prints info about the function running.
    * taq_function_header_print_plot - prints info about the plot.
    * taq_start_folders - creates folders to save data and plots.
    * taq_business_days - creates a list of week days for a year.
    * taq_decompress - decompress original data format to CSV file.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# -----------------------------------------------------------------------------
# Modules

from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
import pickle
import subprocess

# -----------------------------------------------------------------------------


def taq_save_data(function_name, data, ticker_i, ticker_j, year, month, day):
    """ Saves computed data in pickle files.

    Saves the data generated in the functions of the
    taq_data_analysis_article_reproduction module in pickle files.

    :param function_name: name of the function that generates the data.
    :param data: data to be saved. The data can be of different types.
    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :param month: string of the month to be analized (i.e '07').
    :param day: string of the day to be analized (i.e '07').
    :return: None -- The function saves the data in a file and does not return a
     value.
    """

    # Saving data

    if (not os.path.isdir('../../taq_data/article_reproduction_data_{1}/{0}/'
                          .format(function_name, year))):

        try:

            os.mkdir('../../taq_data/article_reproduction_data_{1}/{0}/'
                     .format(function_name, year))
            print('Folder to save data created')

        except FileExistsError:

            print('Folder exists. The folder was not created')

    # Cross-response data
    if (ticker_i != ticker_j):

        pickle.dump(data, open(''.join((
            '../../taq_data/article_reproduction_data_{3}/{0}/{0}_{3}{4}{5}'
            + '_{1}i_{2}j.pickle').split())
            .format(function_name, ticker_i, ticker_j, year, month, day),
            'wb'))

    # Self-response data
    else:

        pickle.dump(data, open(''.join((
            '../../taq_data/article_reproduction_data_{2}/{0}/{0}_{2}{3}{4}'
            '_{1}.pickle').split())
            .format(function_name, ticker_i, year, month, day), 'wb'))

    print('Data Saved')
    print()

    return None

# -----------------------------------------------------------------------------


def taq_save_plot(function_name, figure, ticker_i, ticker_j, year, month):
    """Saves plot in png files.

    Saves the plot generated in the functions of the
    taq_data_plot_article_reproduction module in png files.

    :param function_name: name of the function that generates the plot.
    :param figure: figure object that is going to be save.
    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :param month: string of the month to be analized (i.e '07').
    :return: None -- The function save the plot in a file and does not return
     a value.
    """

    # Saving plot

    if (not os.path.isdir('../../taq_plot/article_reproduction_plot_{1}/{0}/'
                          .format(function_name, year))):

        try:

            os.mkdir('../../taq_plot/article_reproduction_plot_{1}/{0}/'
                     .format(function_name, year))
            print('Folder to save data created')

        except FileExistsError:

            print('Folder exists. The folder was not created')

    # Cross-response
    if (ticker_i != ticker_j):

        figure.savefig(''.join((
            '../../taq_plot/article_reproduction_plot_{3}/{0}/{0}_{3}{4}_{1}i'
            + '_{2}j.png').split())
            .format(function_name, ticker_i, ticker_j, year, month))

    # Self-response
    else:

        figure.savefig(''.join((
            '../../taq_plot/article_reproduction_plot_{2}/{0}/{0}_{2}{3}_{1}i'
            + '.png').split())
            .format(function_name, ticker_i, year, month))

    print('Plot saved')
    print()

    return None

# -----------------------------------------------------------------------------


def taq_function_header_print_data(function_name, ticker_i, ticker_j, year,
                                   month, day):
    """Prints a header of a function that generates data when it is running.

    :param function_name: name of the function that generates the data.
    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :param month: string of the month to be analized (i.e '07').
    :param day: string of the day to be analized (i.e '07').
    :return: None -- The function prints a message and does not return a
     value.
    """

    print('TAQ data')
    print(function_name)

    # Cross-response
    if (ticker_i != ticker_j):
        print('Processing data for the stock i ' + ticker_i + ' and stock j '
              + ticker_j + ' the ' + year + '.' + month + '.' + day)
    # Self-response
    else:
        print('Processing data for the stock ' + ticker_i + ' the ' + year
              + '.' + month + '.' + day)

    return None

# -----------------------------------------------------------------------------


def taq_function_header_print_plot(function_name, ticker_i, ticker_j, year,
                                   month, day):
    """Prints a header of a function that generates a plot when it is running.

    :param function_name: name of the function that generates the plot.
    :param ticker_i: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param ticker_j: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2016').
    :param month: string of the month to be analized (i.e '07').
    :param day: string of the day to be analized (i.e '07').
    :return: None -- The function prints a message and does not return a
     value.
    """

    print('TAQ data')
    print(function_name)

    if (ticker_i != ticker_j):
        print('Processing plot for the stock i ' + ticker_i + ' and stock j '
              + ticker_j + ' the ' + year + '.' + month + '.' + day)
    else:
        print('Processing plot for the stock ' + ticker_i + ' the ' + year
              + '.' + month + '.' + day)

    return None

# -----------------------------------------------------------------------------


def taq_start_folders(year):
    """Creates the initial folders to save the data and plots.

    :param year: string of the year to be analized (i.e '2016').
    :return: None -- The function create folders and does not return a value.
    """

    if (not os.path.isdir('../../taq_data')):

        try:
            os.mkdir('../../taq_data/')
            os.mkdir('../../taq_data/csv_year_data_{}'.format(year))
            os.mkdir('../../taq_data/pickle_dayly_data_{}'.format(year))
            print('Folder to save data created')

        except FileExistsError:
            print('Folder exists. The folder was not created')

    if (not os.path.isdir('../../taq_plot')):

        try:
            os.mkdir('../../taq_plot/')
            print('Folder to save data created')

        except FileExistsError:
            print('Folder exists. The folder was not created')

    if (not os.path.isdir('../../taq_data/article_reproduction_data_{}'
                          .format(year))):

        try:
            os.mkdir('../../taq_data/article_reproduction_data_{}'
                     .format(year))
            print('Folder to save data created')

        except FileExistsError:
            print('Folder exists. The folder was not created')

    if (not os.path.isdir('../taq_plot/article_reproduction__plot{}'
                          .format(year))):

        try:
            os.mkdir('../taq_plot/taq_article_reproduction_plot_{}'
                     .format(year))
            print('Folder to save plot created')

        except FileExistsError:
            print('Folder exists. The folder was not created')

    return None

# -----------------------------------------------------------------------------


def taq_bussiness_days(year):
    """Generate a list with the dates of the bussiness days in a year

    :param year: string of the year to be analized (i.e '2008').
    :return: list.
    """

    init_date = '01/01/{}'.format(year)
    last_date = '12/31/{}'.format(year)

    # Use only the bussiness days
    dt = pd.date_range(start=init_date, end=last_date, freq='B')
    dt_df = dt.to_frame(index=False)
    date_list = dt_df[0].astype(str).tolist()

    return date_list

# -----------------------------------------------------------------------------


def taq_decompress(ticker, year, type):
    """Decompress original data format to CSV file.

    :param ticker: string of the abbreviation of the stock to be analized
     (i.e. 'AAPL').
    :param year: string of the year to be analized (i.e '2008').
    :param type: string with the word 'quotes' or 'trades'.
    :return: None -- The function run a code and does not return a value.
    """

    if (type == 'quotes'):
        subprocess.call('./decompress.out {}_{}_NASDAQ.quotes'
                        .format(ticker, year) +
                        ' > {}_{}_NASDAQ_trades.csv'
                        .format(ticker, year),
                        shell=True, stdout=subprocess.PIPE)

    elif (type == 'trades'):
        subprocess.call('./decompress.out {}_{}_NASDAQ.trades'
                        .format(ticker, year) +
                        ' > {}_{}_NASDAQ_trades.csv'
                        .format(ticker, year),
                        shell=True, stdout=subprocess.PIPE)

    return None

def main():
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """

    pass

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()

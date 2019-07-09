'''
TAQ data analysis

Module to compute the following data

- Self response function: using the midpoint price and the trade signs
  calculate the midpoint log returns and the self response of a stock.

- Cross response function: using the midpoint price and the trade signs
  calculate the midpoint log returns and the cross response between two
  stocks.

Compare the differences between the two definitions of returns (midpoint price
returns and midpoint price log-returns).

The parameter ret can be 'norm' for normalized returns and 'log' for
logarithmic returns.

Juan Camilo Henao Londono
juan.henao-londono@stud.uni-due.de
'''

# ----------------------------------------------------------------------------
# Modules

import numpy as np
import os

import pandas as pd
import pickle

import taq_data_tools

__tau__ = 1000

# ----------------------------------------------------------------------------


def taq_self_response_day_responses_time_shift_data(ticker, date, shift, *,
                                                    tau='off'):
    """
    Obtain the self response function using the midpoint price returns
    and trade signs of the ticker during different time lags. Return an
    array with the self response for a day and an array of the number of
    trades for each value of tau.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param date: string with the date of the data to be extracted
         (i.e. '2008-01-02')
    """

    date_sep = date.split('-')

    year = date_sep[0]
    month = date_sep[1]
    day = date_sep[2]

    function_name = taq_self_response_day_responses_time_shift_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, month, day)

    try:

        # Load data
        midpoint = pickle.load(open(''.join((
                '../../taq_data/article_reproduction_data_{1}/taq_midpoint'
                + '_full_time_data/taq_midpoint_full_time_data_midpoint_{1}'
                + '{2}{3}_{0}.pickle').split())
                .format(ticker, year, month, day), 'rb'))
        trade_sign = pickle.load(open("".join((
                '../../taq_data/article_reproduction_data_{1}/taq_trade_signs'
                + '_full_time_data/taq_trade_signs_full_time_data_{1}{2}{3}_'
                + '{0}.pickle').split())
                .format(ticker, year, month, day), 'rb'))

        # As the data is loaded from the original reproduction data from the
        # article, the data have a shift of 1 second. To correct this I made
        # both data to have the same time [34801, 56999]
        midpoint = midpoint[1:]
        trade_sign = trade_sign[:-1]

        assert len(midpoint) == len(trade_sign)

        # Array of the average of each tau. 10^3 s used by Wang
        self_response_tau = np.zeros(__tau__)
        num = np.zeros(__tau__)

        # Calculating the midpoint log return and the self response function

        # Depending on the tau value

        if (tau == 'off'):
            for tau_idx in range(__tau__):

                if (shift != 0):
                    midpoint_shift = midpoint[:-shift]
                    trade_sign_shift = trade_sign[shift:]
                else:
                    midpoint_shift = midpoint
                    trade_sign_shift = trade_sign

                trade_sign_tau = trade_sign_shift[:-tau_idx - 1]
                trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
                num[tau_idx] = trade_sign_no_0_len
                # Obtain the midpoint log return. Displace the numerator tau
                # values to the right and compute the return

                # Midpoint price returns

                log_return_sec = (midpoint_shift[tau_idx + 1:]
                                  - midpoint_shift[:-tau_idx - 1]) \
                    / midpoint_shift[:-tau_idx - 1]

                # Obtain the self response value
                if (trade_sign_no_0_len != 0):
                    product = log_return_sec * trade_sign_tau
                    self_response_tau[tau_idx] = np.sum(product)

        elif (tau == 'on'):
            for tau_idx in range(__tau__):

                midpoint_shift = midpoint[:-(tau_idx // 2) - 1]
                trade_sign_shift = trade_sign[tau_idx // 2 + 1:]

                assert len(midpoint_shift) == len(trade_sign_shift)

                trade_sign_tau = trade_sign_shift[:-tau_idx - 1]
                trade_sign_no_0_len = len(trade_sign_tau[trade_sign_tau != 0])
                num[tau_idx] = trade_sign_no_0_len
                # Obtain the midpoint log return. Displace the numerator tau
                # values to the right and compute the return

                # Midpoint price returns

                log_return_sec = (midpoint_shift[tau_idx + 1:]
                                  - midpoint_shift[:-tau_idx - 1]) \
                    / midpoint_shift[:-tau_idx - 1]

                # Obtain the self response value
                if (trade_sign_no_0_len != 0):
                    product = log_return_sec * trade_sign_tau
                    self_response_tau[tau_idx] = np.sum(product)

        return self_response_tau, num

    except FileNotFoundError as e:
        print('No data')
        print(e)
        print()
        return None

# ----------------------------------------------------------------------------


def taq_self_response_year_responses_time_shift_data(ticker, year, shift, *,
                                                     tau='off'):
    """
    Obtain the year average self response function using the midpoint
    price returns and trade signs of the ticker during different time
    lags. Return an array with the year average self response.
        :param ticker: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
    """

    function_name = taq_self_response_year_responses_time_shift_data.__name__
    taq_data_tools.taq_function_header_print_data(function_name, ticker,
                                                  ticker, year, '',
                                                  '')

    dates = taq_data_tools.taq_bussiness_days(year)

    self_ = np.zeros(__tau__)
    num_s = []

    for date in dates:

        try:

            (data,
             avg_num) = taq_self_response_day_responses_time_shift_data(
                 ticker, date, shift, tau=tau)

            self_ += data

            num_s.append(avg_num)

        except TypeError:
            pass

    num_s = np.asarray(num_s)
    num_s_t = np.sum(num_s, axis=0)

    # Saving data
    if (tau == 'off'):
        taq_data_tools.taq_save_data('{}_shift_{}'.format(function_name,
                                     shift), self_ / num_s_t, ticker, ticker,
                                     year, '', '')
    elif (tau == 'on'):
        taq_data_tools.taq_save_data('{}_shift_{}'.format(function_name,
                                     'tau'), self_ / num_s_t, ticker, ticker,
                                     year, '', '')

    return self_ / num_s_t, num_s_t

# ----------------------------------------------------------------------------


def taq_cross_response_day_responses_time_shift_data(ticker_i, ticker_j, date,
                                                     shift, *, tau='off'):
    """
    Obtain the cross response function using the midpoint price returns of
    ticker i and trade signs of ticker j during different time lags. The data
    is adjusted to use only the values each second. Return an array with the
    cross response function for a day.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param date: string with the date of the data to be extracted
         (i.e. '2008-01-02')
    """

    if (ticker_i == ticker_j):

        # Self-response

        return None

    else:

        try:

            date_sep = date.split('-')

            year = date_sep[0]
            month = date_sep[1]
            day = date_sep[2]

            function_name = taq_cross_response_day_responses_time_shift_data. \
                            __name__
            taq_data_tools.taq_function_header_print_data(function_name,
                                                          ticker_i, ticker_j,
                                                          year, month, day)

            # Load data
            midpoint_i = pickle.load(open(''.join((
                    '../../taq_data/article_reproduction_data_{1}/taq'
                    + '_midpoint_full_time_data/taq_midpoint_full_time_data'
                    + '_midpoint_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_i, year, month, day), 'rb'))
            trade_sign_j = pickle.load(open("".join((
                    '../../taq_data/article_reproduction_data_2008/taq_trade_'
                    + 'signs_full_time_data/taq_trade_signs_full_time_data'
                    + '_{1}{2}{3}_{0}.pickle').split())
                    .format(ticker_j, year, month, day), 'rb'))

            # As the data is loaded from the original reproduction data from
            # the article, the data have a shift of 1 second. To correct this
            # I made both data to have the same time [34801, 56999]
            midpoint_i = midpoint_i[1:]
            trade_sign_j = trade_sign_j[:-1]

            assert len(midpoint_i) == len(trade_sign_j)

            # Array of the average of each tau. 10^3 s used by Wang
            cross_response_tau = np.zeros(__tau__)
            num = np.zeros(__tau__)

            # Calculating the midpoint return and the cross response function

            # Depending on the tau value

            if (tau == 'off'):
                for tau_idx in range(__tau__):

                    if (shift != 0):
                        midpoint_shift = midpoint_i[:-shift]
                        trade_sign_shift = trade_sign_j[shift:]
                    else:
                        midpoint_shift = midpoint_i
                        trade_sign_shift = trade_sign_j

                    trade_sign_tau = 1 * trade_sign_shift[:-tau_idx - 1]
                    trade_sign_no_0_len = len(
                                           trade_sign_tau[trade_sign_tau != 0])
                    num[tau_idx] = trade_sign_no_0_len
                    # Obtain the midpoint log return. Displace the numerator
                    # tau values to the right and compute the return

                    # Midpoint price returns
                    log_return_i_sec = (midpoint_shift[tau_idx + 1:]
                                        - midpoint_shift[:-tau_idx - 1]) \
                        / midpoint_shift[:-tau_idx - 1]

                    # Obtain the cross response value
                    if (trade_sign_no_0_len != 0):
                        product = log_return_i_sec * trade_sign_tau
                        cross_response_tau[tau_idx] = np.sum(product)

            elif (tau == 'on'):
                for tau_idx in range(__tau__):

                    midpoint_shift = midpoint_i[:-(tau_idx // 2) - 1]
                    trade_sign_shift = trade_sign_j[tau_idx // 2 + 1:]

                    trade_sign_tau = 1 * trade_sign_shift[:-tau_idx - 1]
                    trade_sign_no_0_len = len(
                                          trade_sign_tau[trade_sign_tau != 0])
                    num[tau_idx] = trade_sign_no_0_len
                    # Obtain the midpoint log return. Displace the numerator
                    # tau values to the right and compute the return

                    # Midpoint price returns
                    log_return_i_sec = (midpoint_shift[tau_idx + 1:]
                                        - midpoint_shift[:-tau_idx - 1]) \
                        / midpoint_shift[:-tau_idx - 1]

                    # Obtain the cross response value
                    if (trade_sign_no_0_len != 0):
                        product = log_return_i_sec * trade_sign_tau
                        cross_response_tau[tau_idx] = np.sum(product)

            return cross_response_tau, num

        except FileNotFoundError as e:
            print('No data')
            print(e)
            print()
            return None

# ----------------------------------------------------------------------------


def taq_cross_response_year_responses_time_shift_data(ticker_i, ticker_j, year,
                                                      shift, *, tau='off'):
    """
    Obtain the year average cross response function using the midpoint
    price returns and trade signs of the tickers during different time
    lags. Return an array with the year average cross response.
        :param ticker_i: string of the abbreviation of the midpoint stock to
         be analized (i.e. 'AAPL')
        :param ticker_j: string of the abbreviation of the trade sign stock to
         be analized (i.e. 'AAPL')
        :param year: string of the year to be analized (i.e '2016')
    """

    if (ticker_i == ticker_j):

        # Self-response

        return None

    else:

        function_name = taq_cross_response_year_responses_time_shift_data\
                        .__name__
        taq_data_tools.taq_function_header_print_data(function_name, ticker_i,
                                                      ticker_j, year, '',
                                                      '')

        dates = taq_data_tools.taq_bussiness_days(year)

        cross = np.zeros(__tau__)
        num_c = []

        for date in dates:

            try:

                (data,
                 avg_num) = taq_cross_response_day_responses_time_shift_data(
                     ticker_i, ticker_j, date, shift, tau=tau)

                cross += data

                num_c.append(avg_num)

            except TypeError:
                pass

        num_c = np.asarray(num_c)
        num_c_t = np.sum(num_c, axis=0)

        # Saving data
        if (tau == 'off'):
            taq_data_tools.taq_save_data('{}_shift_{}'.format(function_name,
                                         shift), cross / num_c_t, ticker_i,
                                         ticker_j, year, '', '')
        if (tau == 'on'):
            taq_data_tools.taq_save_data('{}_shift_{}'.format(function_name,
                                         'tau'), cross / num_c_t, ticker_i,
                                         ticker_j, year, '', '')

        return cross / num_c_t, num_c_t

# ----------------------------------------------------------------------------

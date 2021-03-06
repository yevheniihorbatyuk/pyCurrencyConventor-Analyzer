import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime

from tqdm import tqdm
from os import remove

# Sets the start date
today_date = datetime.datetime.today().date()


def get_currency(start_date=None,
                 end_date=None,
                 base='EUR',
                 symbols='RUB',
                 amount='1', format='csv', ):
    # Request function
    def request(start_date_r=start_date,
                end_date_r=end_date,
                base_r=base,
                symbols_r=symbols,
                amount_r=amount, format_r=format):
        url = f'https://api.exchangerate.host/timeseries?{start_date_r}&{end_date_r}/'
        payload = {'start_date': start_date_r, 'end_date': end_date_r,
                   'base': base_r, 'symbols': symbols_r,
                   'amount': amount_r, 'format': format_r}
        response = requests.get(url, params=payload)
        sub_df = pd.read_csv(response.url, sep=',')
        sub_df.to_csv(f'data/{start_date}_{end_date}_{base}_{symbols}_currency_data_set.csv', header=None, mode='a')

        return sub_df

    # Date and time
    request_date = pd.date_range(start=str(start_date), end=str(end_date)).strftime('%Y-%m-%d')
    request_date_period = request_date
    if request_date.size > 366:
        request_date_period = pd.date_range(start=str(start_date), end=str(end_date),
                                            periods=int((request_date.size / 366) + 2)).strftime('%Y-%m-%d')
    else:
        pass

    # Create directories
    try:
        os.makedirs('data')
    except OSError as e:
        print('./data is EXIST')

    # Clear data
    try:
        os.remove(f'data/{start_date}_{end_date}_{base}_{symbols}_currency_data_set.csv')
        print('Date was be rewrote')

    except:
        print('Not exist')

    # Log
    print('start_date:', start_date, '\n',
          'end_date :', end_date, '\n',
          'request_date.size :', int((request_date.size / 366) + 1), '\n',
          'request_date')

    print('request_date.size :', request_date.size, '\n',
          request_date, '\n',
          request_date_period)

    # Requests
    if request_date.size > 366:
        print("IF")
        for year in tqdm(range(0, request_date_period.size - 1), desc='Loading...'):
            start_date_period = request_date_period[year]
            end_date_period = request_date_period[year + 1]

            request(start_date_period, end_date_period, base, symbols, amount, format)

    else:
        # Requests single (one time)
        request(start_date, end_date, base, symbols, amount, format)


def currency_analysis(file_name):
    # Read data set
    df = pd.read_csv(f'{file_name}', sep=',',
                     names=['index', 'date', 'code', 'rate', 'base', 'start_date', 'end_date'], parse_dates=True)

    print(df)
    # Data engineer
    df.drop('index', axis=1, inplace=True)
    df['rate'] = [x.replace(',', '.') for x in df['rate']]
    df['rate'] = df['rate'].astype(float)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    mean_of_years = df.groupby('year').aggregate({'rate': 'mean'})
    mean_of_years_index = mean_of_years.index.values.astype(str)

    max_of_df_rate = df.groupby('year').aggregate({'rate': 'max'})
    max_of_df_rate_index = max_of_df_rate.index.values.astype(str)
    max_of_df_rate_values = max_of_df_rate['rate'].values

    min_of_df_rate = df.groupby('year').aggregate({'rate': 'min'})
    min_of_df_rate_index = min_of_df_rate.index.values.astype(str)
    min_of_df_rate_value = min_of_df_rate['rate'].values

    # LOG
    print('\n------------------------\n',
          'Head of DataFrame:', '\n',
          df.head(5), '\n\n',

          '\n------------------------\n',
          'Describer of DataFrame:', '\n',
          df['rate'].describe(), '\n\n',

          '\n------------------------\n',
          'Max of years:', '\n',
          max_of_df_rate, '\n',

          '\n------------------------\n',
          'Mean of years:', '\n',
          mean_of_years, '\n'
                         
          '\n------------------------\n',
          'Mean of years:', '\n',
          min_of_df_rate, '\n',

          )



    plt.hist(mean_of_years['rate'])
    plt.subplot(2, 1, 1)
    plt.plot(df['date'], df['rate'])
    plt.subplot(2, 1, 1)
    plt.scatter(mean_of_years_index, mean_of_years['rate'], c='green')

    plt.subplot(2, 1, 2)
    plt.bar(mean_of_years_index, mean_of_years['rate'])
    plt.savefig(f'data/{today_date}plot')
    plt.show()

    return df, df['rate'].describe(), max_of_df_rate, mean_of_years, min_of_df_rate
    # Print main property
    # sub_df = pd.DataFrame([{
    #     'code': [0],
    #     'rate': [0],
    #     'base': [0],
    #     'date': [0],
    #     'year': [0],
    #     'month': [0]
    # }])
    # sub_df = pd.DataFrame()
    # for i in range(0, len(max_of_df_rate_values)):
    #     print(i)
    #     sub_df.append(df[df['rate'] == max_of_df_rate_values[i]],)

    # df['year'] = df['date'].year
    # df.columns = ['A', 'B', 'C', 'D']

    # LOG

    # print(df.iloc[:], '\n\n',
    #       df['rate'].describe(), '\n\n',
    #       df['year'].unique())
    #
    # print(max_of_df_rate.columns.values, '\n',
    #       max_of_df_rate['rate'].values, '\n',
    #       max_of_df_rate_index, '\n',
    #       df[df['rate'] == max_of_df_rate_values[1]], '\n',)

    # # sns.lineplot(x= mean_of_yeasrs.index.values, y=mean_of_yeasrs.rate)
    #
    # # plt.hist(mean_of_yeasrs['rate'])
    # # plt.style.use('ggplot')
    # plt.hist(mean_of_yeasrs['rate'])
    # plt.subplot(2, 1, 1)
    # plt.plot(df['date'], df['rate'])
    # plt.subplot(2, 1, 1)
    # plt.scatter(mean_of_years_index, mean_of_years['rate'], c='green')
    # # plt.subplot(2, 1, 1)
    # # plt.scatter(max_of_df_rate_index, max_of_df_rate, c='red')
    #
    # plt.subplot(2, 1, 2)
    # plt.bar(mean_of_years_index, mean_of_years['rate'])
    # plt.savefig(f'data/{today_date}plot')
    # plt.show()

# def currency_plot(data_set):

# a = 10

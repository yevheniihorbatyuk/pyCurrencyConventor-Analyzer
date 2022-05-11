import os
import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime, timedelta

from tqdm import tqdm
from os import remove


# Sets the start date
today_date = datetime.datetime.today().date()


def get_currency(start_date=None,
                 end_date=None,
                 base='EUR',
                 symbols='RUB',
                 amount='1', format='csv', ):
    # Date and time
    request_date = pd.date_range(start=str(start_date), end=str(end_date)).strftime('%Y-%m-%d')

    # Create directories
    try:
        os.makedirs('my_folder')
    except OSError as e:
        print('./data is EXIST')

    # Clear data
    try:
        os.remove(f'data/{today_date}_currency_data_set.csv')
    except:
        print('Not exist')

    # Log
    print('start_date:', start_date, '\n',
          request_date.values)

    # Requests
    for i in tqdm(range(0, len(request_date)), desc='Loading...'):
        url = f'https://api.exchangerate.host/{request_date[i]}/'
        payload = {'base': base, 'symbols': symbols,
                   'amount': amount, 'format': format}
        response = requests.get(url, params=payload)

        time.sleep(0.1)
        sub_df = pd.read_csv(response.url, sep=',')

        # Save to csv
        sub_df.to_csv(f'data/{today_date}_currency_data_set.csv', header=None, mode='a')

        # # Log
        # if (i == 0):
        #     print('Work', url, payload, '\n',
        #           response.url, '\n', )
        # else:
        #     print(sub_df)
        #     sub_df.iloc[:], '\n')


def currency_analysis():
    # Read data set
    df = pd.read_csv(f'data/{today_date}_currency_data_set.csv', sep=',',
                     names=['zero', 'code', 'rate', 'base', 'date'], parse_dates=True)

    # Data engineer
    df.drop('zero', axis=1, inplace=True)
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
          mean_of_years, '\n')

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

    # sns.lineplot(x= mean_of_yeasrs.index.values, y=mean_of_yeasrs.rate)

    # plt.hist(mean_of_yeasrs['rate'])
    # plt.style.use('ggplot')
    # plt.hist(mean_of_yeasrs['rate'])
    plt.subplot(2, 1, 1)
    plt.plot(df['date'], df['rate'])
    # plt.subplot(2, 1, 1)
    # plt.scatter(mean_of_years_index, mean_of_years['rate'], c='green')
    # plt.subplot(2, 1, 1)
    # plt.scatter(max_of_df_rate_index, max_of_df_rate, c='red')

    plt.subplot(2, 1, 2)
    plt.bar(mean_of_years_index, mean_of_years['rate'])
    plt.savefig(f'data/{today_date}plot')
    plt.show()

# def currency_plot(data_set):

# a = 10

#!/usr/bin/env python
# coding: utf-8

# In[2]:

import pandas as pd
import datetime

# creating a dataframe from a csv file
df = pd.read_csv('C:/Users/golik/Google Диск/Разное/Работа/Поиск работы 2022/Improvado home tasks/best_salesman_homework.csv', sep = ',')

# converting the data type in the "date" column to a date
df['date'] = df['date'].astype('datetime64')


# calculate the average duration of deals

# grouping events by client-manager pair
df_delta = df.pivot_table(index = ['client_account_id', 'manager_id'], columns = 'event_name', values = 'date').reset_index()

# remove deals in which there is no start or end date
df_delta = df_delta[~(df_delta['deal'].isnull()) & ~(df_delta['first_touch'].isnull())]

# calculate the duration between start and end
df_delta['delta'] = df_delta['deal'] - df_delta['first_touch']
df_delta['delta_days'] = df_delta['delta'].dt.days.astype('int16')

# remove deals with negative duration (most likely these are new deals for the same client)
df_delta = df_delta[df_delta['delta_days'] >= 0]

# average duration
avg_delta = df_delta['delta_days'].mean().round()


# date of report
report_date = df['date'].max()

# the end date of the period for the first touch
end_date = report_date - datetime.timedelta(days = avg_delta)

# filtering events
df = df[(df['event_name'] == 'deal') | (df['date'] <= end_date)]

# grouping events by manager and type
df_managers = df.groupby(['manager_nickname', 'event_name']).count().reset_index().rename(columns = {'client_account_id':'events'})

# creating a pivot table
df_managers = df_managers.pivot_table(index = 'manager_nickname', columns = 'event_name', values = 'events').reset_index()

# calculating conversions
df_managers['conversion'] = df_managers['deal'] / df_managers['first_touch']
print(df_managers)

# calculating the total conversion
print (f"Total conversion: {(df_managers['deal'].sum() / df_managers['first_touch'].sum()):.3f}")

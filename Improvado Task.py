#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd

# creating a dataframe from a csv file
df = pd.read_csv('C:/Users/golik/Google Диск/Разное/Работа/Поиск работы 2022/Improvado home tasks/best_salesman_homework.csv', sep = ',')

'''
After the first superficial analysis, we see that for all successful deals there is also a record of the first touch. That is, there are no successful transactions in the reporting period that were initiated before it began.  
Therefore, we can include all successful deals in the conversion calculation.  
Let's group the deals by managers and calculate the conversion rate for each of them.
'''

# converting the data type in the "date" column to a date
df['date'] = df['date'].astype('datetime64')

# determine the earliest date of the event for each manager
df_earliest_event = df.groupby('manager_nickname').date.min()

# determine the date from which actions will be taken into account - the latest start of work from all managers
start_date = df_earliest_event.max()

# remove events earlier than the start date
df = df[df['date'] >= start_date]
# print(df.sort_values('date'))

# grouping events by manager and type
df_managers = df.groupby(['manager_nickname', 'event_name']).count().reset_index().rename(columns = {'client_account_id':'events'})

# creating a pivot table
df_managers = df_managers.pivot_table(index = 'manager_nickname', columns = 'event_name', values = 'events').reset_index()

# calculating conversions
df_managers['conversion'] = df_managers['deal'] / df_managers['first_touch']
print(df_managers)

# calculating the total conversion
print (f"Total conversion: {(df_managers['deal'].sum() / df_managers['first_touch'].sum()):.3f}")

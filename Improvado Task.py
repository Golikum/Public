#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# In[3]:


# creating a dataframe from a csv file
df = pd.read_csv('C:/Users/golik/Google Диск/Разное/Работа/Поиск работы 2022/Improvado home tasks/best_salesman_homework.csv', sep = ',')
df.head()


# After the first superficial analysis, we see that for all successful deals there is also a record of the first touch. That is, there are no successful transactions in the reporting period that were initiated before it began.  
# Therefore, we can include all successful deals in the conversion calculation.  
# Let's group the deals by managers and calculate the conversion rate for each of them.

# In[20]:


# grouping events by manager and type
df_managers = df.groupby(['manager_nickname', 'event_name']).count().reset_index().rename(columns = {'client_account_id':'events'})
df_managers


# In[23]:


# creating a pivot table
df_managers = df_managers.pivot_table(index = 'manager_nickname', columns = 'event_name', values = 'events').reset_index()


# In[25]:


# calculating conversions
df_managers['conversion'] = df_managers['deal'] / df_managers['first_touch']
df_managers


# In[29]:


df_managers['deal'].sum()


# In[34]:


# calculating the total conversion

print (f"Total conversion: {(df_managers['deal'].sum() / df_managers['first_touch'].sum()):.3f}")


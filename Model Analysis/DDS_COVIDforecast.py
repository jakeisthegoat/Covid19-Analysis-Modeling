#!/usr/bin/env python
# coding: utf-8

# In[45]:


#import libraries
import csv
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import statistics
import glob


# In[65]:


#actual COVID-19 cases data for PA
url2 = 'https://raw.githubusercontent.com/IvanVoinovGitHub/Covid19-Analysis-Modeling/main/Data/COVID-19_Aggregate_Cases_Current_Daily_County_Health.csv'
df1 = pd.read_csv(url2)


# In[66]:


#reading all the raw data, filtering PA cases data, and ensemble back into one dataframe
path = "/Users/dantr/Downloads/DDSmodel_rawdata/*.csv"
all_data = []
for fname in glob.glob(path):
    df3=pd.read_csv(fname)
    df2_case = df3[df3['target'].str.contains('case')]
    df2_casesPA = df2_case[(df2_case["type"]=="point") & (df2_case["location"]=="42")]
    all_data.append(df2_casesPA)


# In[67]:


df2 = pd.concat(all_data)
df2


# In[72]:


#convert date to datetime object
df1['Date'] = pd.to_datetime(df1['Date'])
df2['forecast_date'] = pd.to_datetime(df2['forecast_date'])
df2['target_end_date'] = pd.to_datetime(df2['target_end_date'])


# In[73]:


#sort datasets by date
df1.sort_values(by='Date')
df2.sort_values(by='target_end_date')


# In[75]:


#need to group the Actual Daily Cases for PA by date
df1_groupedbydate = df1.groupby(["Date"]).sum()
print(df1_groupedbydate)


# In[84]:


df1_groupedbydate[df1_groupedbydate['Date'].dt.date.astype(str) == '2020-08-01']


# In[53]:


#filterinng out data for PA (FIPS code = 42)
df[df["target_end_date"]=='2021-04-17']


# In[ ]:





# In[ ]:





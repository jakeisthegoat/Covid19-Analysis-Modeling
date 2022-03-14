#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import libraries
import csv
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import statistics
import glob


# In[2]:


#actual COVID-19 cases data for PA
url2 = 'https://raw.githubusercontent.com/IvanVoinovGitHub/Covid19-Analysis-Modeling/main/Data/COVID-19_Aggregate_Cases_Current_Daily_County_Health.csv'
df1 = pd.read_csv(url2)


# In[3]:


#reading all the raw data, filtering PA cases data, and ensemble back into one dataframe
path = "/Users/dantr/Downloads/DDSmodel_rawdata/*.csv"
all_data = []
for fname in glob.glob(path):
    df3=pd.read_csv(fname)
    df2_case = df3[df3['target'].str.contains('case')]
    df2_casesPA = df2_case[(df2_case["type"]=="point") & (df2_case["location"]=="42")]
    all_data.append(df2_casesPA)


# In[4]:


df2 = pd.concat(all_data)
df2


# In[5]:


#convert date to datetime object
df1['Date'] = pd.to_datetime(df1['Date'])
df2['forecast_date'] = pd.to_datetime(df2['forecast_date'])
df2['target_end_date'] = pd.to_datetime(df2['target_end_date'])


# In[6]:


#sort datasets by date
df1.sort_values(by='Date')
df2.sort_values(by='target_end_date')


# In[8]:


#need to group the Actual Daily Cases for PA by date
df1_groupedbydate = df1.groupby(["Date"]).sum()
df1_groupedbydate


# In[9]:


#filterinng out data for PA (FIPS code = 42)
df2_2 = df2[df2['target'].str.contains('1')]
df2_2.shape


# In[10]:


#finding weekly increase in cases in PA
df_weekly=df2_2.groupby('target_end_date').agg('last').reset_index()
df_weekly.rename(
    columns={"target_end_date":"Date"},inplace=True)
df_weekly


# In[11]:


df_weekly.dtypes


# In[12]:


df1_groupedbydate.dtypes


# In[ ]:


#creating a column for daily additions
df_weekly["dayRate"] = df_weekly["value"] / 7
df_weekly


# In[ ]:


merged_weekly = pd.merge(left=df1_groupedbydate[['Cumulative cases                          ']], right=df_weekly, left_on='Date', right_on='Date')
merged_weekly.rename(columns={'Cumulative cases                          ':'Cumulative cases'}, inplace=True)
merged_weekly


# In[ ]:


merged_weekly.shape


# In[ ]:


#select all the dates to be merged with prediction table
mask = (df1['Date'] > '2020-08-01') & (df1['Date'] <= '2021-04-03')
df1_copy = df1.loc[mask]
df1_copy = df1_copy.groupby(["Date"]).sum()
df1_copy.rename(columns={'Cumulative cases                          ':'Cumulative cases'}, inplace=True)
df1_copy


# In[ ]:


merged_df = df1_copy[['Cumulative cases']].merge(df_weekly, how='left', left_on = 'Date', right_on = 'Date')
merged_df.head(10)


# In[ ]:


#generate the rest of the rows to fill in between bi-weekly data 
merged_df_new = merged_df
for i, row in merged_df.iterrows():
    for _ in range(6):
        merged_df_new.at[i,'location']="42"


# In[ ]:


merged_df_new = merged_df_new.fillna(method='bfill')
merged_df_new.head(20)


# In[ ]:


merged_df_new.shape


# In[ ]:


merged_df_new = pd.merge(merged_df_new, merged_weekly, on='Date', how='left')
merged_df_new.drop(['forecast_date_y', 'location_y', 
                'target_y', 'type_y','quantile_y','value_y','dayRate_y'], axis=1, inplace=True)


# In[ ]:


merged_df_new.rename(columns={'Cumulative cases_x':'Cumulative cases', 'forecast_date_x':'forecast_date',
                             'location_x':'location','target_x':'target','type_x':'type',
                             'quantile_x':'quantile','value_x':'value','dayRate_x':'dayRate'}, inplace=True)
merged_df_new.head(20)


# In[ ]:


merged_inner.to_csv('DDS_weekly_predictions.csv')


# In[ ]:


merged_df_new.dtypes





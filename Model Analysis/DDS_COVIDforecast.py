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


# In[13]:


merged_inner = pd.merge(left=df1_groupedbydate[['Cumulative cases                          ']], right=df_weekly, left_on='Date', right_on='Date')
merged_inner


# In[ ]:


print(df1_groupedbydate)


# In[ ]:


#creating a column for daily additions
df_weekly["dayRate"] = df_weekly["value"] / 7


# In[ ]:


#Merge Datasets on Data attribute
merged_weekly = pd.merge(left=df_weekly, right=df1_groupedbydate, left_on='target_end_date', right_on='Date')
merged_weekly


# In[ ]:


#creating a column for daily additions
df_weekly["dayRate"] = df_weekly["Cumulative cases"] * 1.882


# In[15]:


merged_inner.to_csv('DDS_weekly_predictions.csv')


# In[ ]:





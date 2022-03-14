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


#fill out all weekly the empty dayRate rows with the same average dayRate
merged_df_new = merged_df_new.fillna(method='bfill')
merged_df_new.head(20)


# In[19]:


merged_df_new.shape


# In[20]:


#merging actual cases and predcited by week
merged_df_new = pd.merge(merged_df_new, merged_weekly, on='Date', how='left')
merged_df_new.drop(['forecast_date_y', 'location_y', 
                'target_y', 'type_y','quantile_y','value_y','dayRate_y'], axis=1, inplace=True)


# In[21]:


merged_df_new.rename(columns={'Cumulative cases_x':'Cumulative cases', 'forecast_date_x':'forecast_date',
                             'location_x':'location','target_x':'target','type_x':'type',
                             'quantile_x':'quantile','value_x':'value','dayRate_x':'dayRate'}, inplace=True)
merged_df_new.head(40)


# In[22]:


merged_df_new.shape


# In[23]:


merged_df_new.dtypes


# In[43]:


#filling out all the days of the week with predicted values from the model
for i in range(6, 245, 7):
    merged_df_new2.at[i-1,'Cumulative cases_y']=merged_df_new2.at[i,'Cumulative cases_y'] - merged_df_new2.at[i,'dayRate']
    merged_df_new2.at[i-2,'Cumulative cases_y']=merged_df_new2.at[i-1,'Cumulative cases_y'] - merged_df_new2.at[i,'dayRate']
    merged_df_new2.at[i-3,'Cumulative cases_y']=merged_df_new2.at[i-2,'Cumulative cases_y'] - merged_df_new2.at[i,'dayRate']
    merged_df_new2.at[i-4,'Cumulative cases_y']=merged_df_new2.at[i-3,'Cumulative cases_y'] - merged_df_new2.at[i,'dayRate']
    merged_df_new2.at[i-5,'Cumulative cases_y']=merged_df_new2.at[i-4,'Cumulative cases_y'] - merged_df_new2.at[i,'dayRate']
    merged_df_new2.at[i-6,'Cumulative cases_y']=merged_df_new2.at[i-5,'Cumulative cases_y'] - merged_df_new2.at[i,'dayRate']


# In[58]:


#filling missing values
merged_df_new2['Cumulative cases_y'] = merged_df_new2['Cumulative cases_y'].fillna(method='ffill')


# In[47]:


merged_df_new2.tail(10)


# In[61]:


#renaming columns for predcited and actual cases
merged_df_new2.rename(columns={'Cumulative cases':'Actual', 'Cumulative cases_y':'Prediction'}, inplace=True)
merged_df_new2.head(10)


# In[63]:


#Create plot of Actual vs. Predicted Cases

#Actual Cases Line
plt.plot(merged_df_new2['Date'], merged_df_new2['Actual'], color='g', label='Actual Cases')

#Predicted Cases Line
plt.plot(merged_df_new2['Date'], merged_df_new2['Prediction'], color='r', label='Predicted Cases')

#Create XY Labels and Title
plt.xlabel('Date (Year/Month/Day)') 
plt.ylabel('Number of Cases') 
plt.title("Predicted Daily Cases vs Actual Cases in PA")

#Display Plot
plt.legend()
plt.show()


# In[64]:


#error calculations
#confirmed = merged_df_new2['Actual']
#projected = merged_df_new2['Prediction']
error = []
rawerror = []

for index, row in merged_df_new2.iterrows():
  rawerror.append(-1*(row['Actual'] - row["Prediction"]) / row['Actual'])
  error.append((abs(row['Actual'] - row["Prediction"])) / row['Actual'])

underpredictCount = 0
overpredictCount = 0
for x in rawerror:
  if x < 0:
    underpredictCount += 1
  elif x > 0:
    overpredictCount += 1

underpredictPerecentage = underpredictCount / len(rawerror)
overpredictPercentage = 1 - underpredictPerecentage

print(underpredictCount)
print(underpredictPerecentage)
print(overpredictCount)
print(overpredictPercentage)
print(len(error))

print(error)
print(rawerror)


# In[65]:


#accuracy calculations
accuracy = []

for i in error:
  accuracy.append(1 - i)

print(accuracy)


# In[66]:


#Create Error and Accuracy Column and insert list data
merged_df_new2['Error'] = error
merged_df_new2['Accuracy'] = accuracy
merged_df_new2['RawError'] = rawerror

print(merged_df_new2)


# In[67]:


from IPython.core.pylabtools import figsize
#Create plot of Error

#Error Line
plt.plot(merged_df_new2['Date'], merged_df_new2['Error'], color='g', label='Error')


#Create XY Labels and Title
plt.xlabel('Date (Year/Month/Day)') 
plt.ylabel('Percentage') 
plt.title("Predicted Daily COVID-19 Case Error in PA")
#Display Plot
plt.legend()


# In[68]:


#Create plot of Raw Error

#Raw Error Line
plt.plot(merged_df_new2['Date'], merged_df_new2['RawError'], color='g', label='Raw Error')
plt.axhline(y=0.0, color='r', linestyle='-')

#Create XY Labels and Title
plt.xlabel('Date (Year/Month/Day)') 
plt.ylabel('Percentage') 
plt.title("Predicted Daily COVID-19 Case Raw Error in PA")
#Display Plot
plt.legend()
plt.show()


# In[69]:


#Create plot of Accuracy

#Accuracy Line
plt.plot(merged_df_new2['Date'], merged_df_new2['Accuracy'], color='r', label='Daily Accuracy')

#Create XY Labels and Title
plt.xlabel('Date (Year/Month/Day)') 
plt.ylabel('Percentage') 
plt.title("Predicted Daily COVID-19 Case Accuracy in PA")

#Display Plot
plt.legend()
plt.show()


# In[71]:


#Calculate Weekly Accuracy Averages
weeklyAccuracy = 0
averageWeeklyAccuracy = []
length = len(accuracy)
amountOfWeeks = int(length / 7)
remainderDays = length % 7

i = 0
while i < length:
  weeklyAccuracy += accuracy[i]
  if (i + 1) % 7 == 0 and amountOfWeeks > 0:
    averageWeeklyAccuracy.append(weeklyAccuracy / 7)
    amountOfWeeks -= 1
    weeklyAccuracy = 0
  if (i + 1) % remainderDays == 0 and remainderDays > 0 and amountOfWeeks == 0:
    averageWeeklyAccuracy.append(weeklyAccuracy / remainderDays)
    weeklyAccuracy = 0
  i += 1

weeklyDateList = []
i = 0
weeklyDateList.append(merged_df_new2['Date'][i])
while i < length:
  if (i + 1) % 7 == 0:
    weeklyDateList.append(merged_df_new2['Date'][i])
  i += 1


# In[72]:


#Create Dataframe for Weekly Accuracy
i = 0
data = []
while i < len(averageWeeklyAccuracy):
  data.append([weeklyDateList[i], averageWeeklyAccuracy[i]])
  i += 1

df = pd.DataFrame(data, columns = ['Week Of', 'Average Weekly Accuracy'])


# In[62]:


merged_df_new2.to_csv('DDS_everyday_predictions.csv')


# In[ ]:





# In[ ]:


merged_df_new.dtypes





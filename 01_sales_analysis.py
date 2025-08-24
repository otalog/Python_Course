# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# JUMPSTART (Module 1): First Sales Analysis with Python ----

# Important VSCode Set Up:
#   1. Select a Python Interpreter: ds4b_101p
#   2. Delete terminals to start a fresh Python Terminal session

# 1.0 Load Libraries ----

# %%
# load library
# %% [markdown]
# # Core Python Data Analysis
import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# Plotting 
from plotnine import (
    ggplot,
    aes,
    geom_col, geom_line,geom_smooth,facet_wrap,
    scale_y_continuous,scale_x_datetime, labs, theme,theme_minimal,
    theme_matplotlib
)# plotnine is python package as ggplot in R, from plotnine import helps us to import speci
#fic module rather than loading all the functions

from mizani.breaks import date_breaks # ploting scale package in R
from mizani.formatters import date_format, currency_format

# %%
# Misc
from os import mkdir,getcwd #from os means the package id coming from the operating system of python
from rich import pretty # used for better terminal formating. Contains the pretty module
pretty.install() # the install() is a fxn located in the pretty module within the rich package
np.sum([1,2,3]) 

# 2.0 Importing Data Files ----
# %%
help(pd.read_excel)
# - Use "q" to quit
# %%

getcwd()

# %%

bikes_df=pd.read_excel("00_data_raw/bikes.xlsx")
bikes_df

bikeshops_df=pd.read_excel("00_data_raw/bikeshops.xlsx")

bikeshops_df

orderlines_df=pd.read_excel("00_data_raw/orderlines.xlsx")

orderlines_df=pd.read_excel(
    io="00_data_raw/orderlines.xlsx",
    converters= {'order.date':str})
orderlines_df.info()



# 3.0 Examining Data ----
# %%
bikes_df.head(15)
orderlines_df
bikeshops_df

# %%
s=bikes_df['description']#seleceting a particular column
freq_count=s.value_counts()#counts the appearance of each description
freq_count.nlargest()# the largers count in asc. order

# %%
#method chain using periof(.)
bikes_df['description'].value_counts().nlargest()
topfive_bike_series=bikes_df['description'].value_counts().nlargest()
fig=topfive_bike_series.plot(kind='barh')
fig.invert_yaxis()# this inverts the graph
pd.Series.plot(topfive_bike_series)
plt.show()
#?pd.Series.plot#run in iteraction mode
# 4.0 Joining Data ----
#%%
orderlines_df=pd.DataFrame(orderlines_df)# Convert to dataframe before droping

orderlines_df.drop(columns='Unnamed: 0',axis=1)

orderlines_df \
    .drop(columns='Unnamed: 0',axis=1) # drop a column
    
#merging
bike_orderlines_joined_df=orderlines_df \
    .drop(columns='Unnamed: 0',axis=1) \
        .merge(
            right=bikes_df,
            how ='left',
            left_on='product.id',
            right_on='bike.id'
        )\
            .merge(
                right=bikeshops_df,
                how='left',
                left_on='customer.id',
                right_on='bikeshop.id'
                
            )
bike_orderlines_joined_df

# 5.0 Wrangling Data ----

# * No copy
df=bike_orderlines_joined_df

# * Copy
df2=bike_orderlines_joined_df.copy()

df2.info()
# * Handle Dates
df['order.date']
df['order.date']=pd.to_datetime(df['order.date'])
df.info()
# * Show Effect: Copy vs No Copy
bike_orderlines_joined_df.info()

# * Text Columns
df.description # for data description
df.T # do this to transpose
df.head().T# do this to for larger tables
 

# * Splitting Description into category_1, category_2, and frame_material

"Mountain - Over Mountain - Carbon".split(" - ") 
df['description'].str.split() # Pandas series has accessor depending on the data type; 
#?pd.Series.str.split
#text(string) has str
#DateTime has dt
#categorical has cat
temp_df=df['description'].str.split(pat='- ', expand =True)# expand split them in columns
df['category.1'] =temp_df[0]# put first split series in first column
df['category.2'] =temp_df[1]#put in another column 
df['frame.material']=temp_df[2]
df
# * Splitting Location into City and State
temp_df=df['location'].str.split(', ', n=1, expand=True)# N=1 means 1 split
temp_df

df['city']=temp_df[0]
df['state']=temp_df[1]
df

# * Price Extended
df.T# give detailes of the table
df['total.price']=df['quantity']*df['price']
df
df.sort_values('total.price',ascending=False)#ascending total price columns



# * Reorganizing
df.columns#returns all the columns

cols_to_keep_list=['order.id', 
 'order.line', 
 'order.date', 
 #'customer.id', 
 #'product.id',
 #'quantity', 
 #'bike.id', 
 'model', 
 #'description', 
 'quantity',
 'price', 
 'total.price',
 #'bikeshop.id',
 'bikeshop.name', 
 'location', 
 'category.1', 
 'category.2', 
 'frame.material',
 'city', 
 'state'
]

df=df[cols_to_keep_list]
# * Renaming columns
df['order.date']# how to call individual columns of a dataframe
'order.date'.replace(".", "_")#str.replace() is a builtin function that modifies a string by replacing patterns of text with a replacement
#it replaces dot with underscore
df.columns=df.columns.str.replace(".", "_")# replace all column names with dot with underscore
#these two returns the same output
df.order_id
df['order_id']

#%%
bike_orderlines_joined_df
bike_orderlines_wrangle_df=df
bike_orderlines_wrangle_df#clean data after wrangling
# 6.0 Visualizing a Time Series ----
mkdir("00_data_wrangled")
bike_orderlines_wrangle_df.to_pickle("00_data_wrangled/bike_orderlines_wrangled_df.pkl")
df=pd.read_pickle("00_data_wrangled/bike_orderlines_wrangled_df.pkl")

# 6.1 Total Sales by Month ----
df=pd.DataFrame(df)
df['order_date']
order_date_series=df['order_date']
df['order_date'].dt.year

  #Y for year agrregation, df.aggregate() use summary fxn to cols of DF, works with resamples and groups
df[['order_date','total_price']] \
    .set_index('order_date') \
    .resample(rule='M') \
    .aggregate(np.sum) #np.sum is numpy sum function 

#  converts any row index to a column, that is convert 1 column df to a 2 col df
#np.sum is numpy sum function 
sales_by_month_df=df[['order_date','total_price']] \
    .set_index('order_date') \
    .resample(rule='M') \
    .aggregate(np.sum) \
    .reset_index()


# Quick Plot ----
#introduction to matplot backend
sales_by_month_df.plot(x='order_date',y='total_price')
plt.show()
usd=currency_format(prefix="$", digits=0, big_mark=",")
usd([1000])
# Report Plot ----
#Use plotnine; a port of the ggplot2 r package, geom_smooth applies trendline
#commom options are; method="lm" or "loess" span =0.5(loess only)
ggplot(aes(x='order_date', y='total_price'),data=sales_by_month_df)+\
    geom_line() +\
    geom_smooth(method='loess',se =False, color="blue",span=0.3)+\
    scale_y_continuous(labels=usd)+\
    labs(
        title="Revenue by Month",
        x="",
        y="Revenue"
    )+\
    theme_minimal()+\
    expand_limits(y=0)

# 6.2 Sales by Year and Category 2 ----

# ** Step 1 - Manipulate ----


# Step 2 - Visualize ----


# Simple Plot


# Reporting Plot



# 7.0 Writing Files ----


# Pickle ----


# CSV ----


# Excel ----


# WHERE WE'RE GOING
# - Building a forecast system
# - Create a database to host our raw data
# - Develop Modular Functions to:
#   - Collect data
#   - Summarize data and prepare for forecast
#   - Run Automatic Forecasting for One or More Time Series
#   - Store Forecast in Database
#   - Retrieve Forecasts and Report using Templates













# %%

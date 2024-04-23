# -*- coding: utf-8 -*-
"""Big mart sales prediction

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1h-7PkLASi2IYFgRq_Sys08J8dazKPxz9

Importing the libaries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics

"""Data collection and analysis"""

# loading the dataset from csv file to Pandas Dataframe
Big_mart_data = pd.read_csv('/content/Train.csv')

# first 5 rows of the Dataframe
Big_mart_data.head()

# number of data points and number of features
Big_mart_data.shape

# getting some information about the datset
Big_mart_data.info()

"""Categorical Features:

-Item_Identifier

-Item_Fat_Content

-Item_Type

-Outlet_Identifier

-Outlet_Size

-Outlet_Location_Type

-Outlet_Type
"""

# checking missing values
Big_mart_data.isnull().sum()

"""Handling missing values

mean > > > average value

mode > > > most repeated value
"""

# mean value of "item weight" column
Big_mart_data['Item_Weight'].mean()

# filling the missing value in "item weight" column with "mean" value
Big_mart_data['Item_Weight'].fillna(Big_mart_data['Item_Weight'].mean(),inplace= True)

# checking missing values
Big_mart_data.isnull().sum()

"""Replacing the missing values in "Outlet size" with mode"""

mode_of_outlet_size = Big_mart_data.pivot_table(values='Outlet_Size',columns = 'Outlet_Type', aggfunc=(lambda x: x.mode()[0]))

print(mode_of_outlet_size)

missing_values = Big_mart_data['Outlet_Size'].isnull()

print(missing_values)

Big_mart_data.loc[missing_values, 'Outlet_Size'] = Big_mart_data.loc[missing_values, 'Outlet_Type'].apply(lambda x: mode_of_outlet_size)

# checking missing values
Big_mart_data.isnull().sum()

"""Data Analysis"""

# statistical measures about the data
Big_mart_data.describe()

"""Numerical Features"""

sns.set()

# Item_weight distribution
plt.figure(figsize=(6,6))
sns.distplot(Big_mart_data['Item_Weight'])
plt.show()

# Item_Visibility distribution
plt.figure(figsize=(6,6))
sns.distplot(Big_mart_data['Item_Visibility'])
plt.show()

#  Item_MRP distribution
plt.figure(figsize=(6,6))
sns.distplot(Big_mart_data['Item_MRP'])
plt.show()

#  Item_Outlet_Sales distribution
plt.figure(figsize=(6,6))
sns.distplot(Big_mart_data['Item_Outlet_Sales'])
plt.show()

# Outlet_Establishment_Year column
plt.figure(figsize=(6,6))
sns.countplot(x='Outlet_Establishment_Year', data=Big_mart_data)
plt.show()

"""Categorical features:"""

#  Item_Fat_Content column
plt.figure(figsize=(6,6))
sns.countplot(x='Item_Fat_Content', data=Big_mart_data)
plt.show()

# Item_Type column
plt.figure(figsize=(30,6))
sns.countplot(x='Item_Type', data=Big_mart_data)
plt.show()

# Outlet_Size_Column
plt.figure(figsize=(6,6))
sns.countplot(x='Outlet_Size', data=Big_mart_data)
plt.show()

"""Data prepocessing"""

Big_mart_data.head()

Big_mart_data['Item_Fat_Content'].value_counts()

Big_mart_data.replace({'Item_Fat_Content': {'low fat':'Low Fat','LF':'Low Fat', 'reg':'Regular'}}, inplace=True)

Big_mart_data['Item_Fat_Content'].value_counts()

"""Label Encoding"""

Encoder = LabelEncoder()

Big_mart_data['Item_Identifier'] = Encoder.fit_transform(Big_mart_data['Item_Identifier'])

Big_mart_data['Item_Fat_Content'] = Encoder.fit_transform(Big_mart_data['Item_Fat_Content'])

Big_mart_data['Item_Type'] = Encoder.fit_transform(Big_mart_data['Item_Type'])

Big_mart_data['Outlet_Identifier'] = Encoder.fit_transform(Big_mart_data['Outlet_Identifier'])

Big_mart_data['Outlet_Size'] = Encoder.fit_transform(Big_mart_data['Outlet_Size'])

Big_mart_data['Outlet_Location_Type'] = Encoder.fit_transform(Big_mart_data['Outlet_Location_Type'])

Big_mart_data['Outlet_Type'] = Encoder.fit_transform(Big_mart_data['Outlet_Type'])

Big_mart_data.head()

"""Splitting Features and target"""

X = Big_mart_data.drop(columns='Item_Outlet_Sales', axis=1)
Y = Big_mart_data['Item_Outlet_Sales']

print(X)

print(Y)

"""Splitting the data into training data and testing data"""

X_train, X_test , Y_train, Y_test = train_test_split(X , Y, test_size=0.2, random_state=2)

print(X.shape, X_train.shape, X_test.shape)

"""Machine Learning Model Training

XGBoost Regressor
"""

regressor = XGBRegressor()

regressor.fit(X_train, Y_train)

"""Evaluation"""

# prediction on training data
training_data_prediction = regressor.predict(X_train)

# R squared value
r2_train = metrics.r2_score(Y_train,training_data_prediction)

print( 'R squared value =', r2_train)

# prediction on test data
test_data_prediction = regressor.predict(X_test)

# R squared Value
r2_test = metrics.r2_score(Y_test, test_data_prediction)

print('R Squared value = ', r2_test)

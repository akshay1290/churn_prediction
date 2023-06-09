# -*- coding: utf-8 -*-
"""churn_model_building.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HtmjCeiyCjH0WNJrTBU_QIQe4EdheBHH

# **Predicting Customer Churn in a Telecom Company**

# 1. **Problem statement**

A telecom company is facing a high customer churn rate and wants to reduce it. Customer churn refers to the process where a customer stops doing business with a company. In the telecom industry, customer churn is a major problem as acquiring new customers is more expensive than retaining existing customers. The company wants to use machine learning to predict which customers are likely to churn so that they can take proactive measures to retain them.
"""

# Commented out IPython magic to ensure Python compatibility.
#import the required libraries
import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.ticker as mtick  
import matplotlib.pyplot as plt
# %matplotlib inline
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from imblearn.combine import SMOTEENN

"""#**2. Import necessary libraries and load the dataset**"""

df = pd.read_csv('/content/train.csv')
df1 = pd.read_csv('/content/test.csv')

df.head()

df1.head()

df.info()

df1.info()

## checking the percentage of nan values present in each feature

features_with_na=[features for features in df.columns if df[features].isnull().sum()>1]

for feature in features_with_na:
    print(feature, np.round(df[feature].isnull().mean(), 4),  ' % missing values')

df.isnull().sum()

df1.isnull().sum()

df1.columns

# Check the  Statistical Numerical Data Distribution Summary
df.describe()

df1.describe()

df.corr() # the correlation between the columns

# Correlation of the columns shown in a heatmap
plt.figure(figsize=(15,15))
sns.heatmap(df.corr(),annot=True);

# Identifying the unique number of values in the dataset
df.nunique()

df1.nunique()

df=df.drop('customerID',axis=1)

# defining numerical & categorical columns
numeric_features = [feature for feature in df.columns if df[feature].dtype != 'O']
categorical_features = [feature for feature in df.columns if df[feature].dtype == 'O']

# print columns
print('We have {} numerical features : {}'.format(len(numeric_features), numeric_features))
print('\nWe have {} categorical features : {}'.format(len(categorical_features), categorical_features))

# defining numerical & categorical columns
numeric_features = [feature for feature in df1.columns if df1[feature].dtype != 'O']
categorical_features = [feature for feature in df1.columns if df1[feature].dtype == 'O']

# print columns
print('We have {} numerical features : {}'.format(len(numeric_features), numeric_features))
print('\nWe have {} categorical features : {}'.format(len(categorical_features), categorical_features))

df['Churn'] = np.where(df.Churn == 'Yes',1,0)

# Import label encoder 
from sklearn import preprocessing 
  
# label_encoder object knows how to understand word labels. 
label_encoder = preprocessing.LabelEncoder() 

df['gender']= label_encoder.fit_transform(df['gender'])
df['Partner']= label_encoder.fit_transform(df['Partner'])

df['Dependents']= label_encoder.fit_transform(df['Dependents'])
df['PhoneService']= label_encoder.fit_transform(df['PhoneService'])

df['MultipleLines']= label_encoder.fit_transform(df['MultipleLines'])
df['InternetService']= label_encoder.fit_transform(df['InternetService'])
df['OnlineSecurity']= label_encoder.fit_transform(df['OnlineSecurity'])
df['OnlineBackup']= label_encoder.fit_transform(df['OnlineBackup'])
df['DeviceProtection']= label_encoder.fit_transform(df['DeviceProtection'])
df['TechSupport']= label_encoder.fit_transform(df['TechSupport'])

df['StreamingTV']= label_encoder.fit_transform(df['StreamingTV'])
df['StreamingMovies']= label_encoder.fit_transform(df['StreamingMovies'])
df['Contract']= label_encoder.fit_transform(df['Contract'])
df['PaperlessBilling']= label_encoder.fit_transform(df['PaperlessBilling'])
df['PaymentMethod']= label_encoder.fit_transform(df['PaymentMethod'])
df['TotalCharges']= label_encoder.fit_transform(df['TotalCharges'])

# Import label encoder 
from sklearn import preprocessing 
  
# label_encoder object knows how to understand word labels. 
label_encoder = preprocessing.LabelEncoder() 

df1['gender']= label_encoder.fit_transform(df1['gender'])
df1['Partner']= label_encoder.fit_transform(df1['Partner'])

df1['Dependents']= label_encoder.fit_transform(df1['Dependents'])
df1['PhoneService']= label_encoder.fit_transform(df1['PhoneService'])

df1['MultipleLines']= label_encoder.fit_transform(df1['MultipleLines'])
df1['InternetService']= label_encoder.fit_transform(df1['InternetService'])
df1['OnlineSecurity']= label_encoder.fit_transform(df1['OnlineSecurity'])
df1['OnlineBackup']= label_encoder.fit_transform(df1['OnlineBackup'])
df1['DeviceProtection']= label_encoder.fit_transform(df1['DeviceProtection'])
df1['TechSupport']= label_encoder.fit_transform(df1['TechSupport'])

df1['StreamingTV']= label_encoder.fit_transform(df1['StreamingTV'])
df1['StreamingMovies']= label_encoder.fit_transform(df1['StreamingMovies'])
df1['Contract']= label_encoder.fit_transform(df1['Contract'])
df1['PaperlessBilling']= label_encoder.fit_transform(df1['PaperlessBilling'])
df1['PaymentMethod']= label_encoder.fit_transform(df1['PaymentMethod'])
df1['TotalCharges']= label_encoder.fit_transform(df1['TotalCharges'])

# Identify the columns with potential outliers
outlier_cols = ['SeniorCitizen', 'tenure', 'MonthlyCharges','TotalCharges']

# Replace outliers with the upper and lower bounds
for col in outlier_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    upper_bound = q3 + 1.5*iqr
    lower_bound = q1 - 1.5*iqr
    df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])
    df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])

# Identify the columns with potential outliers
outlier_cols = ['SeniorCitizen', 'tenure', 'MonthlyCharges','TotalCharges']

# Replace outliers with the upper and lower bounds
for col in outlier_cols:
    q1 = df1[col].quantile(0.25)
    q3 = df1[col].quantile(0.75)
    iqr = q3 - q1
    upper_bound = q3 + 1.5*iqr
    lower_bound = q1 - 1.5*iqr
    df1[col] = np.where(df1[col] > upper_bound, upper_bound, df1[col])
    df1[col] = np.where(df1[col] < lower_bound, lower_bound, df1[col])

#checking outiliers in dataset
fig, axs = plt.subplots(ncols=11, nrows=2, figsize=(20, 10))
index = 0
axs = axs.flatten()
for k,v in df.items():
    sns.boxplot(y=k, data= df, ax=axs[index])
    index += 1
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=5.0)

df.columns

df1.columns

"""# **3. Model Building**"""

x=df.drop('Churn',axis=1)

x

y=df['Churn']
y

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)

model_dt=DecisionTreeClassifier(criterion = "gini",random_state = 100,max_depth=6, min_samples_leaf=8)

model_dt.fit(x_train,y_train)

y_pred=model_dt.predict(x_test)
y_pred

model_dt.score(x_test,y_test)

print(classification_report(y_test, y_pred, labels=[0,1]))

from sklearn.ensemble import RandomForestClassifier
model_rf=RandomForestClassifier(n_estimators=100, criterion='gini', random_state = 100,max_depth=6, min_samples_leaf=8)

model_rf.fit(x_train,y_train)

y_pred=model_rf.predict(x_test)

model_rf.score(x_test,y_test)

print(classification_report(y_test, y_pred, labels=[0,1]))

"""***Oversampling To balence the data***"""

print("Before OverSampling, counts of label '1': {}".format(sum(y_train==1)))
print("Before OverSampling, counts of label '0': {} \n".format(sum(y_train==0)))

from imblearn.combine import SMOTEENN

sm = SMOTEENN()
X_resampled, y_resampled = sm.fit_resample(x, y)

print('After OverSampling, the shape of train_X: {}'.format(X_resampled.shape))
print('After OverSampling, the shape of train_y: {} \n'.format(y_resampled.shape))

print("After OverSampling, counts of label '1': {}".format(sum(y_resampled==1)))
print("After OverSampling, counts of label '0': {}".format(sum(y_resampled==0)))

xr_train1,xr_test1,yr_train1,yr_test1=train_test_split(X_resampled, y_resampled,test_size=0.2,random_state=42)

model_rf_smote=RandomForestClassifier(n_estimators=100, criterion='gini', random_state = 100,max_depth=6, min_samples_leaf=8)
model_rf_smote.fit(xr_train1,yr_train1)

model_rf_smote.score(xr_train1,yr_train1)

from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import f1_score
y_pred_rf_smote = model_rf_smote.predict(xr_test1)
print("Accuracy of random forest model:", accuracy_score(yr_test1, y_pred_rf_smote))
print("Confusion matrix of random forest model:\n", confusion_matrix(yr_test1, y_pred_rf_smote))
print("classification_report of random forest  model:\n",classification_report(yr_test1, y_pred_rf_smote, labels=[0,1]))
f1 = f1_score(yr_test1, y_pred_rf_smote)
print("F1 score:", f1)

"""# ***Random Forest Classifier model applying on balenced data***

# ***Downloding Pickle file***
"""

### Create a Pickle file using serialization 
import pickle
pickle_out = open("model_rf_smote.pkl","wb")
pickle.dump(model_rf_smote, pickle_out)
pickle_out.close()

df.head()

df1.head()

model_rf.predict([[0,0.0,1,0,1.0,0,0,0,0,2,0,0,0,0,0,1,2,29.85,2505.0]])

y_pred = model_rf_smote.predict_proba([[0,0.0,0,0,11.802333,1,1,1,0,0,0,0,0,1,0,1,1,81.032399,674.301500]])[0, 1]
churn = y_pred >= 0.5
output_prob = float(y_pred)
output = bool(churn)
print(output_prob)
print(output)

y_pred = model_rf_smote.predict_proba(df1)[0, 1]
churn = y_pred >= 0.5
output_prob = float(y_pred)
output = bool(churn)
print(output_prob)
print(output)
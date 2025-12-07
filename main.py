import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

dataset = pd.read_csv("UberDataset.csv")
dataset.head()
dataset.shape
dataset.info()

#data preprocessing
dataset['PURPOSE'] = dataset['PURPOSE'].fillna("NOT")
dataset['START_DATE'] = pd.to_datetime(dataset['START_DATE'], errors='coerce')
dataset['END_DATE'] = pd.to_datetime(dataset['END_DATE'], errors='coerce')

from datetime import datetime

dataset['date'] = pd.DatetimeIndex(dataset['START_DATE']).date
dataset['time'] = pd.DatetimeIndex(dataset['START_DATE']).hour

#changing into categories of day and night
dataset['day-night'] = pd.cut(x=dataset['time'],
                              bins = [0,10,15,19,24],
                              labels = ['Morning','Afternoon','Evening','Night'])

dataset.dropna(inplace=True)
dataset.drop_duplicates(inplace=True)

#data visualization
obj = (dataset.dtypes == 'object')
object_cols = list(obj[obj].index)

unique_values = {}
for col in object_cols:
  unique_values[col] = dataset[col].unique().size
unique_values

plt.figure(figsize=(10,5)) #the countplot for CATEGORY and PURPOSE columns
plt.subplot(1,2,1)
sns.countplot(x='CATEGORY', data=dataset)
plt.xticks(rotation=90)
plt.title('Category column Counts')
plt.subplot(1,2,2)
purpose_order = dataset['PURPOSE'].value_counts().index
sns.countplot(x='PURPOSE', data=dataset, order=purpose_order)
plt.xticks(rotation=90)
plt.title('Purpose column Counts')
plt.tight_layout()

plt.figure(figsize=(10,5)) #countplot for TIME column
sns.countplot(x='day-night', data=dataset)
plt.xticks(rotation=90)
plt.title('Time Column Counts')
plt.tight_layout()

#comparing the two different categories along with the PURPOSE of the user.
plt.figure(figsize=(15, 5))
sns.countplot(data=dataset, x='PURPOSE', hue='CATEGORY')
plt.xticks(rotation=90)
plt.title('Comparison of different categories wrt purpose')
plt.tight_layout()

from sklearn.preprocessing import OneHotEncoder 
object_cols = ['CATEGORY', 'PURPOSE']            #using onehotcoder to categorize CATEGORY and PURPOSE
OH_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
OH_cols = pd.DataFrame(OH_encoder.fit_transform(dataset[object_cols]))
OH_cols.index = dataset.index
OH_cols.columns = OH_encoder.get_feature_names_out()
df_final = dataset.drop(object_cols, axis=1)
dataset = pd.concat([df_final, OH_cols], axis=1)


numeric_dataset = dataset.select_dtypes(include=['number'])
plt.figure(figsize=(10,5))
sns.heatmap(numeric_dataset.corr(), 
            cmap='BrBG', 
            fmt='.2f', 
            linewidths=2, 
            annot=True,
            annot_kws={"size": 8})
plt.title('Correlation Matrix of CATEGORY and PURPOSE')
plt.tight_layout()

#visualization of month data
dataset['MONTH'] = pd.DatetimeIndex(dataset['START_DATE']).month
month_label = {1.0: 'Jan', 2.0: 'Feb', 3.0: 'Mar', 4.0: 'April',
               5.0: 'May', 6.0: 'June', 7.0: 'July', 8.0: 'Aug',
               9.0: 'Sep', 10.0: 'Oct', 11.0: 'Nov', 12.0: 'Dec'}
dataset["MONTH"] = dataset.MONTH.map(month_label)
mon = dataset.MONTH.value_counts(sort=False)

df = pd.DataFrame({"Ride Counts": mon.values,
                   "Distance Travelled": dataset.groupby('MONTH', sort=False)['MILES'].max()
                   })
plt.figure(figsize=(10, 6)) # Month total rides count vs Month ride max count
p = sns.lineplot(data=df)
p.set(xlabel="MONTHS", ylabel="VALUE COUNT")
plt.title('Max Miles Traveled per Month vs. Total Ride Counts') 
plt.xticks(rotation=45)

#Visualization for days data
dataset['DAY'] = dataset.START_DATE.dt.weekday
day_label = {
    0: 'Mon', 1: 'Tues', 2: 'Wed', 3: 'Thus', 4: 'Fri', 5: 'Sat', 6: 'Sun'
}
dataset['DAY'] = dataset['DAY'].map(day_label)
day_label = dataset.DAY.value_counts()
plt.figure(figsize=(10, 6)) #count of rides per day
sns.barplot(x=day_label.index, y=day_label);
plt.xlabel('DAY')
plt.ylabel('COUNT')
plt.title('Count of rides per weekday')

plt.figure(figsize=(10, 5)) #Visualization for miles data
plt.subplot(1,2,1)
sns.boxplot(dataset['MILES'])
plt.title('Boxplot of MILES')
plt.subplot(1,2,2)
sns.boxplot(dataset[dataset['MILES']<100]['MILES'])
plt.title('Boxplot of MILES value less than 100')
plt.tight_layout()

plt.figure(figsize=(10, 5))
sns.distplot(dataset[dataset['MILES']<40]['MILES'])
plt.title('Distribution of MILES value less than 40')
plt.tight_layout()
plt.show()
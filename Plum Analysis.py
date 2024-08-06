# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 14:18:59 2024

@author: VALUE
"""

import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel("C:/Users/VALUE/Downloads/plum/DA Assignment.xlsx")

df.info()
df.isnull().sum()

# Impute missing values for numerical columns with median
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())

# Impute missing values for categorical columns with mode
categorical_cols = df.select_dtypes(include=['object']).columns
df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])

# Impute missing values for datetime columns with forward fill (ffill)
datetime_cols = df.select_dtypes(include=['datetime64[ns]']).columns
df[datetime_cols] = df[datetime_cols].fillna(method='ffill')

# Alternatively, you can also use specific default date for datetime columns
# df[datetime_cols] = df[datetime_cols].fillna(pd.to_datetime('2022-01-01'))

# Check if there are still any missing values
print(df.isnull().sum())

# pandas plot() function with parameters kind = 'box' and subplots = True
categorical_features = df.select_dtypes(include = ['object']).columns
print(categorical_features)


# Segregating Numeric features
numeric_features = df.select_dtypes(exclude = ['object','datetime64[ns]']).columns
print(numeric_features)

# Convert index to DataFrame
df = df.reset_index(drop=True)

a = df.head(20)

df.plot(kind = 'box', subplots = True, sharey = False, figsize = (25, 18))

# Increase spacing between subplots
plt.subplots_adjust(wspace = 0.75)  


'''sharey True or 'all': x- or y-axis will be shared among all subplots.
False or 'none': each subplot x- or y-axis will be independent.'''


from feature_engine.outliers import Winsorizer

winsor_iqr = Winsorizer(capping_method = 'iqr', 
                        # choose  IQR rule boundaries or gaussian for mean and std
                          tail = 'both', # cap left, right or both tails 
                          fold = 1.5, 
                          variables = ['Requester wait time in minutes within business hours'])

df['Requester wait time in minutes within business hours']= winsor_iqr.fit_transform(df[['Requester wait time in minutes within business hours']])



# Instantiate Winsorizer with 'iqr' capping method and 'both' tail
# Specify a higher fold value for more aggressive treatment if needed
winsor_iqr = Winsorizer(capping_method='quantiles', tail='both', fold=0.05, variables=['Reopens'])

# Apply Winsorization to the DataFrame
df['Reopens'] = winsor_iqr.fit_transform(df[['Reopens']])

df.info()
# Save the cleaned DataFrame to a CSV file in the current working directory
df.to_csv('cleaned_data.csv', index=False)

df.plot(kind = 'box', subplots = True, sharey = False, figsize = (25, 18))

# Increase spacing between subplots
plt.subplots_adjust(wspace = 0.75)  


import matplotlib.pyplot as plt
import seaborn as sns

# Assuming your DataFrame is named 'df'

# Visualization 1: Bar Chart for Status Distribution
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='Status')
plt.title('Status Distribution')
plt.xlabel('Status')
plt.ylabel('Count')
plt.show()

# Visualization 2: Bar Chart for Priority Distribution
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='Priority')
plt.title('Priority Distribution')
plt.xlabel('Priority')
plt.ylabel('Count')
plt.show()

# Visualization 3: Line Chart for Resolution Time Trends
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x=df.index, y='Resolution time')
plt.title('Resolution Time Trends')
plt.xlabel('Index')
plt.ylabel('Resolution Time')
plt.show()

# Visualization 4: Histogram for Resolution Time Distribution
plt.figure(figsize=(8, 6))
sns.histplot(data=df, x='Resolution time', bins=10, kde=True)
plt.title('Resolution Time Distribution')
plt.xlabel('Resolution Time')
plt.ylabel('Count')
plt.show()

# Visualization 5: Box Plot for Reopens Distribution
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='Reopens')
plt.title('Reopens Distribution')
plt.xlabel('Reopens')
plt.show()

# Visualization 6: Stacked Bar Chart for Status and Priority
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Status', hue='Priority')
plt.title('Status and Priority Distribution')
plt.xlabel('Status')
plt.ylabel('Count')
plt.legend(title='Priority')
plt.show()

# Visualization 7: Time Series Analysis for Requester Wait Time
# Assuming 'Created at' column is available as datetime
df['Created at'] = pd.to_datetime(df['Created at'])
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='Created at', y='Requester wait time in minutes')
plt.title('Requester Wait Time Trends')
plt.xlabel('Date')
plt.ylabel('Requester Wait Time (minutes)')
plt.show()

# Visualization 8: Heatmap for Correlation Analysis
plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

###part 2 questions
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming your DataFrame is named 'df'

# Step 1: Calculate average resolution time for each group
average_resolution_time = df.groupby('Group')['Resolution time'].mean().reset_index()

# Step 2: Create a table displaying the average resolution time for each group
print("Average Resolution Time by Group:")
print(average_resolution_time)

# Step 3: Visualize average resolution time using a bar chart
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Group', y='Resolution time', palette='Set2')
plt.title('Average Resolution Time by Group')
plt.xlabel('Group')
plt.ylabel('Average Resolution Time')
plt.xticks(rotation=45)
plt.show()


##Question 3

# Assuming 'df' is your DataFrame

# Step 1: Calculate average resolution time for each unique combination of 'Group', 'Status', and 'Priority'
avg_resolution_time = df.groupby(['Group', 'Status', 'Priority'])['Resolution time'].mean().reset_index()

# Step 2: Create a table displaying the average resolution time for each combination
print("Average Resolution Time by Ticket Type:")
print(avg_resolution_time)

# Step 3: Visualize average resolution time using a bar chart
plt.figure(figsize=(12, 6))
sns.barplot(data=avg_resolution_time, x='Resolution time', y='Group', hue='Status', palette='Set2')
plt.title('Average Resolution Time by Ticket Type')
plt.xlabel('Average Resolution Time')
plt.ylabel('Group')
plt.show()


from scipy.stats import ttest_ind, f_oneway

# Assuming 'df' is your DataFrame

# Perform t-tests or ANOVA to assess differences in resolution times between different groups or categories
# For example, comparing resolution times between different ticket statuses
resolved = df[df['Status'] == 'Solved']['Resolution time']
closed = df[df['Status'] == 'Closed']['Resolution time']

t_stat, p_value = ttest_ind(resolved, closed)
print("T-test Results:")
print("T-statistic:", t_stat)
print("P-value:", p_value)

# Alternatively, you can use ANOVA to compare resolution times across multiple groups (e.g., ticket priorities)
anova_result = f_oneway(df[df['Priority'] == 'High']['Resolution time'],
                        df[df['Priority'] == 'Low']['Resolution time'])
print("\nANOVA Results:")
print("F-statistic:", anova_result.statistic)
print("P-value:", anova_result.pvalue)

# Check for missing values in 'Resolution time' column
missing_values = df['Resolution time'].isnull().sum()
if missing_values > 0:
    print("Warning: There are missing values in the 'Resolution time' column. Handle missing values before proceeding.")
else:
    # Perform ANOVA only if there are no missing values
    anova_result = f_oneway(df[df['Priority'] == 'High']['Resolution time'],
                            df[df['Priority'] == 'Low']['Resolution time'])
    print("\nANOVA Results:")
    print("F-statistic:", anova_result.statistic)
    print("P-value:", anova_result.pvalue)
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('C:/Users/Seethalakshmi1/AppData/Local/Programs/Python/Python313/user_behavior_dataset.csv')
#list out columns of the data set
columns = df.columns.tolist()
print("Columns in the Dataset: ",columns)
#print how many records are available in dataset
num_records = df.shape[0]
print(f"\n Number of records: {num_records}")
#display top5 list of the list
top_5_records = df.head()
print("\n Top 5 records of the Dataset: \n")
print(top_5_records,"\n")
#check the presence of missing values
missing_values = df.isnull().sum()
print("Check the number of missing elements in each column: \n")
print(missing_values)
#Insert a new column "Memory usage (MB)" after the column "Battery drain", thendelete it.
df.insert(df.columns.get_loc('Battery Drain (mAh/day)') + 1, 'Memory usage (MB)',0) # Insert with dummy values
df.drop(columns=['Memory usage (MB)'], inplace=True) # Delete the column
#Find the maximum value of 1.app usage time, 2.screen on time, 3.battery draintime,4.number of apps installed
# app usage
max_app_usage_time = df['App Usage Time (min/day)'].max()
print(f"\n Max App Usage Time: {max_app_usage_time}")
# screen on time
max_screen_on_time = df['Screen On Time (hours/day)'].max()
print(f"\n Max Screen on Time: {max_screen_on_time}")
# battery drain time
max_battery_drain_time = df['Battery Drain (mAh/day)'].max()
print(f"\n Max Battery Drain Time: {max_battery_drain_time}")

# number of apps installed
max_apps_installed = df['Number of Apps Installed'].max()
print(f"\n Max Number of Apps Installed: {max_apps_installed}")
#Find the range of Age(Maximum age and Minimum age)
min_age = df['Age'].min()
max_age = df['Age'].max()
print(f"\n Age Range: {min_age} - {max_age}")
#Device models available in dataset
num_device_models = df['Device Model'].nunique()
print(f"\n Number of device models: {num_device_models}")
#OS available in the dataset
operating_systems = df['Operating System'].unique()
print("\n Operating system: ",operating_systems)
#Find average battery drain time and No.of Apps installed
avg_battery_drain_time = df['Battery Drain (mAh/day)'].mean()
avg_apps_installed = df['Number of Apps Installed'].mean()
print(f"\n Average Battery Drain Time: {avg_battery_drain_time}")
print(f"\n Average Number of Apps Installed: {avg_apps_installed} \n")
#Drop a row if it contains any null valueimport pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('user_behavior_dataset.csv')
#list out columns of the data set
columns = df.columns.tolist()
print("Columns in the Dataset: ",columns)
#print how many records are available in dataset
num_records = df.shape[0]
print(f"\n Number of records: {num_records}")
#display top5 list of the list
top_5_records = df.head()
print("\n Top 5 records of the Dataset: \n")
print(top_5_records,"\n")
#check the presence of missing values
missing_values = df.isnull().sum()

print("Check the number of missing elements in each column: \n")
print(missing_values)
#Insert a new column "Memory usage (MB)" after the column "Battery drain", then delete it.
df.insert(df.columns.get_loc('Battery Drain (mAh/day)') + 1, 'Memory usage (MB)',
0) # Insert with dummy values
df.drop(columns=['Memory usage (MB)'], inplace=True) # Delete the column
#Find the maximum value of 1.app usage time, 2.screen on time, 3.battery draintime,4.number of apps installed
# app usage
max_app_usage_time = df['App Usage Time (min/day)'].max()
print(f"\n Max App Usage Time: {max_app_usage_time}")
# screen on time
max_screen_on_time = df['Screen On Time (hours/day)'].max()
print(f"\n Max Screen on Time: {max_screen_on_time}")
# battery drain time
max_battery_drain_time = df['Battery Drain (mAh/day)'].max()
print(f"\n Max Battery Drain Time: {max_battery_drain_time}")
# number of apps installed
max_apps_installed = df['Number of Apps Installed'].max()
print(f"\n Max Number of Apps Installed: {max_apps_installed}")
#Find the range of Age(Maximum age and Minimum age)
min_age = df['Age'].min()
max_age = df['Age'].max()
print(f"\n Age Range: {min_age} - {max_age}")
#Device models available in dataset
num_device_models = df['Device Model'].nunique()
print(f"\n Number of device models: {num_device_models}")
#OS available in the dataset
operating_systems = df['Operating System'].unique()
print("\n Operating system: ",operating_systems)
#Find average battery drain time and No.of Apps installed
avg_battery_drain_time = df['Battery Drain (mAh/day)'].mean()
avg_apps_installed = df['Number of Apps Installed'].mean()

print(f"\n Average Battery Drain Time: {avg_battery_drain_time}")
print(f"\n Average Number of Apps Installed: {avg_apps_installed} \n")
#Drop a row if it contains any null value
df_cleaned = df.dropna()
#plot the pie chart for various categories of users(1 to 5)
user_categories = df['User Behavior Class'].value_counts()
plt.pie(user_categories, labels=user_categories.index, autopct='%1.1f%%',
startangle=90)
plt.axis('equal') # Equal aspect ratio ensures that pie chart is circular
plt.title('User Categories Distribution')
plt.show()
df_cleaned = df.dropna()
#plot the pie chart for various categories of users(1 to 5)
user_categories = df['User Behavior Class'].value_counts()
plt.pie(user_categories, labels=user_categories.index, autopct='%1.1f%%',
startangle=90)
plt.axis('equal') # Equal aspect ratio ensures that pie chart is circular
plt.title('User Categories Distribution')
plt.show()

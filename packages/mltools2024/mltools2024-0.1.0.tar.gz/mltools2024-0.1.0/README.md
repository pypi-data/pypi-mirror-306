#ml 1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
#We do not want to see warnings
warnings.filterwarnings("ignore")

data = pd.read_csv("uber.csv")

df = data.copy()

df.head

df.info()

df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])

df.info()

df.describe()
df.isnull().sum()
df.drop(['key', 'Unnamed: 0'],axis = 1,inplace=True)
df2=df.drop(["pickup_datetime"],axis = 1)
df2
df2.corr()

fig,axis = plt.subplots(figsize = (10,6))
sns.heatmap(df2.corr(),annot = True)

df.dropna(inplace=True)
df.plot(kind = "box",subplots = True,layout = (7,2),figsize=(15,20)) #Boxplot shows that dataset is free from outliers


def remove_outlier(df1, col):
    Q1 = df1[col].quantile(0.25)
    Q3 = df1[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_whisker = Q1 - 1.5 * IQR
    upper_whisker = Q3 + 1.5 * IQR
    df[col] = np.clip(df1[col], lower_whisker, upper_whisker)
    return df1


def treat_outliers_all(df1, col_list):
    for c in col_list:
        df1 = remove_outlier(df, c)
    return df1


df = treat_outliers_all(df, df.iloc[:, 0::])

df.plot(kind="box", subplots=True, layout=(7, 2), figsize=(15, 20))  # Boxplot shows that dataset is free from outliers

#Check the missing values now
df.isnull().sum()

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

datatime_column = df['pickup_datetime']
df.drop('pickup_datetime', axis=1, inplace=True)

# Scale the DataFrame without the datetime column
standard_scaler = StandardScaler()
df_scaled_array = standard_scaler.fit_transform(df)

# Convert the scaled array back to a DataFrame
df_scaled = pd.DataFrame(df_scaled_array, columns=df.columns)

# Add the pickup_datetime column back
df_scaled['pickup_datetime'] = datatime_column.reset_index(drop=True)

#Take x as predictor variable
x = df_scaled.drop("fare_amount", axis = 1)
#And y as target variable
y = df_scaled['fare_amount']

x['pickup_datetime'] = pd.to_numeric(pd.to_datetime(x['pickup_datetime']))

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 1)

from sklearn.linear_model import LinearRegression

lrmodel = LinearRegression()
lrmodel.fit(x_train, y_train)

predict = lrmodel.predict(x_test)

from sklearn.metrics import mean_squared_error , r2_score
lrmodelrmse = np.sqrt(mean_squared_error(y_test,predict))
r2 = r2_score(y_test,predict)
print("RMSE error for the model is ", lrmodelrmse)
print("R2 score for the model is ", r2)

#Let's Apply Random Forest Regressor
from sklearn.ensemble import RandomForestRegressor
rfrmodel = RandomForestRegressor(n_estimators = 100, random_state = 101)

#Fit the Forest
rfrmodel.fit(x_train, y_train)
rfrmodel_pred = rfrmodel.predict(x_test)

#Errors for the forest
rfrmodel_rmse = np.sqrt(mean_squared_error(y_test , rfrmodel_pred))
rf_r2 = r2_score(y_test,rfrmodel_pred)
print("RMSE value for Random Forest is:",rfrmodel_rmse)
print("R2 score for the model is ", rf_r2)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score, recall_score, precision_score,accuracy_score


df=pd.read_csv("C://Users//91772//Desktop//ML assigns//diabetes.csv")

df.head()

df.shape
(768, 9)
df.describe()

#replace zeros
zero_not_accepted=["Glucose","BloodPressure","SkinThickness","BMI","Insulin"]
for column in zero_not_accepted:
    df[column]=df[column].replace(0,np.NaN)
    mean=int(df[column].mean(skipna=True))
    df[column]=df[column].replace(np.NaN,mean)

df["Glucose"]

#split dataset
X=df.iloc[:,0:8]
y=df.iloc[:,8]
X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=0,test_size=0.2)

#feature Scaling
sc_X=StandardScaler()
X_train=sc_X.fit_transform(X_train)
X_test=sc_X.transform(X_test)

knn=KNeighborsClassifier(n_neighbors=11)

knn.fit(X_train,y_train)

KNeighborsClassifier(n_neighbors=11)

y_pred=knn.predict(X_test)

#Evaluate The Model
cf_matrix=confusion_matrix(y_test,y_pred)

ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues')
ax.set_title('Seaborn Confusion Matrix with labels\n\n');
ax.set_xlabel('\nPredicted Values')
ax.set_ylabel('Actual Values ');
## Display the visualization of the Confusion Matrix.
plt.show()

tn, fp, fn, tp = confusion_matrix(y_test, y_pred ).ravel()

tn, fp, fn, tp

accuracy_score(y_test,y_pred)

precision_score(y_test,y_pred)

recall_score(y_test,y_pred)

error_rate=1-accuracy_score(y_test,y_pred)

error_rate

2

[1]: import numpy as np
import pandas as pd
[2]: data = pd.read_csv('./diabetes.csv')
data.head()
[4]: #Check for null or missing values
data.isnull().sum()
[6]: #Replace zero values with mean values
for column in data.columns[1:-3]:
data[column].replace(0, np.NaN, inplace = True)
data[column].fillna(round(data[column].mean(skipna=True)), inplace = True)
data.head(10)
[7]: X = data.iloc[:, :8] #Features
Y = data.iloc[:, 8:] #Predictor
[22]: #Perform Spliting
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2,␣
↪random_state=0)

[23]:#KNN
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn_fit = knn.fit(X_train, Y_train.values.ravel())
knn_pred = knn_fit.predict(X_test)

[24]: from sklearn.metrics import confusion_matrix, precision_score, recall_score,␣
↪f1_score, accuracy_score
print("Confusion Matrix")
print(confusion_matrix(Y_test, knn_pred))
print("Accuracy Score:", accuracy_score(Y_test, knn_pred))
print("Reacal Score:", recall_score(Y_test, knn_pred))
print("F1 Score:", f1_score(Y_test, knn_pred))
print("Precision Score:",precision_score(Y_test, knn_pred))

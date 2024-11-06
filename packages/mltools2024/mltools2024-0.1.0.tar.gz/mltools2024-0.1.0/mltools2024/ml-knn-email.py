import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load the dataset
file_path = 'emails.csv'  # Update this path if needed
emails_data = pd.read_csv(file_path)

# Separate features and labels
X = emails_data.drop(columns=['Email No.', 'Prediction'])  # Features (word counts)
y = emails_data['Prediction']  # Labels: 1 for spam, 0 for not spam

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

### K-Nearest Neighbors (KNN) Classifier ###
# Initialize and train the KNN model
knn_model = KNeighborsClassifier(n_neighbors=5)  # You can tune the 'n_neighbors' parameter
knn_model.fit(X_train, y_train)

# Predict on test data
knn_y_pred = knn_model.predict(X_test)

# KNN Performance Metrics
knn_accuracy = accuracy_score(y_test, knn_y_pred)
knn_precision = precision_score(y_test, knn_y_pred)
knn_recall = recall_score(y_test, knn_y_pred)
knn_f1 = f1_score(y_test, knn_y_pred)

print("K-Nearest Neighbors (KNN) Performance:")
print("Accuracy:", knn_accuracy)
print("Precision:", knn_precision)
print("Recall:", knn_recall)
print("F1 Score:", knn_f1)

### Support Vector Machine (SVM) Classifier ###
# Initialize and train the SVM model
svm_model = SVC(kernel='linear', C=1.0)  # Using a linear kernel; adjust 'C' as needed
svm_model.fit(X_train, y_train)

# Predict on test data
svm_y_pred = svm_model.predict(X_test)

# SVM Performance Metrics
svm_accuracy = accuracy_score(y_test, svm_y_pred)
svm_precision = precision_score(y_test, svm_y_pred)
svm_recall = recall_score(y_test, svm_y_pred)
svm_f1 = f1_score(y_test, svm_y_pred)

print("\nSupport Vector Machine (SVM) Performance:")
print("Accuracy:", svm_accuracy)
print("Precision:", svm_precision)
print("Recall:", svm_recall)
print("F1 Score:", svm_f1)

# Comparison Summary
print("\nPerformance Comparison:")
print(f"KNN - Accuracy: {knn_accuracy}, Precision: {knn_precision}, Recall: {knn_recall}, F1 Score: {knn_f1}")
print(f"SVM - Accuracy: {svm_accuracy}, Precision: {svm_precision}, Recall: {svm_recall}, F1 Score: {svm_f1}")

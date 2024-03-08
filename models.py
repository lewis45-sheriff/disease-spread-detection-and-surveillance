import numpy as np
import pandas as pd
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Importing the dataset
datasets = pd.read_csv('csvData.csv')
X = datasets.iloc[:, [1, 2]].values
Y = datasets.iloc[:, 3].values

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Creating a pipeline for preprocessing and model building
pipeline = make_pipeline(StandardScaler(), RandomForestClassifier(random_state=42))

# Define hyperparameters for tuning
param_dist = {
    'randomforestclassifier__n_estimators': [100, 200, 300],
    'randomforestclassifier__max_depth': [10, 20, 30, None],
    'randomforestclassifier__min_samples_split': [2, 5, 10],
    'randomforestclassifier__min_samples_leaf': [1, 2, 4],
    'randomforestclassifier__bootstrap': [True, False]
}

# Performing randomized search cross-validation to find the best hyperparameters
random_search = RandomizedSearchCV(pipeline, param_dist, n_iter=100, cv=5, scoring='accuracy', random_state=42)
random_search.fit(X_train, y_train)

# Best hyperparameters
best_params = random_search.best_params_
print("Best Hyperparameters:", best_params)

# Best model from random search
best_model = random_search.best_estimator_

# Evaluating the model on the test set
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Test Set Accuracy:", accuracy)

# Classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save the model to a pickle file
with open('random_forest_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

# Predicting for a new location
new_data = pd.DataFrame({
    'Population Density': [750],
    'Reported Cases': [1]
})

# Making prediction using the best model
prediction = best_model.predict(new_data)
if prediction[0] == 1:
    print("The disease is likely to occur in this location.")
else:
    print("The disease is not likely to occur in this location.")

# Plotting accuracy metrics
metrics = classification_report(y_test, y_pred, output_dict=True)
accuracy = metrics['accuracy']
precision = metrics['1']['precision']
recall = metrics['1']['recall']
f1_score = metrics['1']['f1-score']

fig = go.Figure(data=[
    go.Bar(name='Metrics', x=['Accuracy', 'Precision', 'Recall', 'F1-Score'], y=[accuracy, precision, recall, f1_score])
])
fig.update_layout(title='Model Performance Metrics',
                  xaxis_title='Metric',
                  yaxis_title='Score',
                  yaxis=dict(range=[0, 1]),
                  barmode='group')
fig.show()

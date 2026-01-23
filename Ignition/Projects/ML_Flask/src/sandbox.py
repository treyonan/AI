# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Specify the path to your .csv file
file_path = 'test_data.csv'
##

# Read the .csv file into a dataframe
df = pd.read_csv(file_path)

# Create a mask where num_actuations is 10 or less
mask = df['num_actuations'] <= 10

# Identify where the reset points are, and use `cumsum` to create groups for separate cumulative sum calculations
groups = mask.cumsum()

# Average the three pressure columns for each row
df['avg_pressure'] = df[['pressure', 'pressure2', 'pressure3']].mean(axis=1)

# For each group, calculate the running average
# Note: We use the transform method to broadcast the result back to the original shape of the DataFrame
df['running_avg'] = df.groupby(groups)['avg_pressure'].transform(lambda x: (x + x.shift(1)) / 2)

# For rows where num_actuations is 10 or less, replace the running average with the current row's avg_pressure
df['running_avg'] = df['running_avg'].where(~mask, df['avg_pressure'])

# Sum the three test_minutes columns for each row
df['test_minutes_sum'] = df[['test_minutes', 'test_minutes2', 'test_minutes3']].sum(axis=1)

# Calculate the cumulative sum within each group
df['test_minutes_cum'] = df.groupby(groups)['test_minutes_sum'].cumsum()

# For rows where num_actuations is 10 or less, replace the cumulative sum with the current row's test_minutes_sum
df['test_minutes_cum'] = df['test_minutes_cum'].where(~mask, df['test_minutes_sum'])

# Display the first few rows of the dataframe to check
print(df.head())

# Features and target variable
X = df[['running_avg', 'test_minutes_cum', 'num_actuations']]
y = df['psi_decay']

# Splitting the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Building the model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Making predictions
y_pred = regressor.predict(X_test)

# Evaluating the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R^2 Score: {r2:.2f}")

plt.scatter(y_test, y_pred, alpha=0.4)
plt.xlabel("actual psi decay")
plt.ylabel("predicted psi decay")
plt.title("Actual psi decay vs. predicted")
plt.show()
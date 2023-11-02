import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# from laptop-
# ----------------------------------

# Specify the path to your .csv file
file_path = 'test_data2.csv'

# Read the .csv file into a dataframe
df = pd.read_csv(file_path)

# Calculate the psi_decay column
df['psi_decay'] = df['Shell Start'] - df['Shell End']

# Create a mask where num_actuations is 10 or less
mask = df['num_actuations'] <= 10

# Identify where the reset points are, and use `cumsum` to create groups for separate cumulative sum calculations
groups = mask.cumsum()

# Average the three pressure columns for each row
df['avg_pressure'] = df[['Shell Start', 'Lower Hydro Start', 'Upper Hydro Start']].mean(axis=1)

# For each group, calculate the running average
# Note: We use the transform method to broadcast the result back to the original shape of the DataFrame
df['running_avg'] = df.groupby(groups)['avg_pressure'].transform(lambda x: (x + x.shift(1)) / 2)

# For rows where num_actuations is 10 or less, replace the running average with the current row's avg_pressure
df['running_avg'] = df['running_avg'].where(~mask, df['avg_pressure'])

# Sum the three minutes columns for each row
df['test_minutes_sum'] = df[['Shell Minutes', 'Lower Hydro Minutes', 'Upper Hydro Minutes']].sum(axis=1)

# Calculate the cumulative sum within each group
df['test_minutes_cum'] = df.groupby(groups)['test_minutes_sum'].cumsum()

# For rows where num_actuations is 10 or less, replace the cumulative sum with the current row's test_minutes_sum
df['test_minutes_cum'] = df['test_minutes_cum'].where(~mask, df['test_minutes_sum'])

# Display the first few rows of the dataframe to check
print(df.head())

# Features and target variable
x = df[['running_avg', 'test_minutes_cum', 'num_actuations']]
#x = df[['test_minutes_cum', 'num_actuations']]
#x = df[['test_minutes_cum']]
y = df['psi_decay']

# Splitting the data into training and testing sets (80% train, 20% test)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Building the model
regressor = LinearRegression()
regressor.fit(x_train, y_train)

# Making predictions
y_pred = regressor.predict(x_test)

# Evaluating the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R^2 Score: {r2:.2f}")
print(f"Coeff: {regressor.coef_}")
print(f"Score: {regressor.score(x_train, y_train)}")

plot = 1

if plot == 1:
    plt.scatter(y_test, y_pred, alpha=0.4)
    plt.xlabel("actual psi decay")
    plt.ylabel("predicted psi decay")
    plt.title("Actual psi decay vs. predicted")
elif plot == 2:
    plt.scatter(df[['test_minutes_cum']], df[['psi_decay']], alpha=0.4)
elif plot == 3:
    # Slicing the dataframe to get every 50th data point
    df_sliced = df[::50]

    # Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(df_sliced.index, df_sliced['psi_decay'], label='psi_decay', color='blue')
    plt.title('psi_decay over Data Points (Every 50th Point)')
    plt.xlabel('Data Point Number')
    plt.ylabel('psi_decay')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plt.show()



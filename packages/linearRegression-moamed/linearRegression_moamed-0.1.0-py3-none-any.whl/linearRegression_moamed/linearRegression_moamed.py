# Import required modules
import numpy as np  # type: ignore
import pandas as pd
import matplotlib.pyplot as plt

# Defining the class


class LinearRegression:
    def __init__(self, x, y):
        self.data = x
        self.label = y
        self.m = 0  # slope
        self.b = 0  # intercept
        self.n = len(x)

    def fit(self, epochs, lr):
        # Implementing Gradient Descent
        for i in range(epochs):
            y_pred = self.m * self.data + self.b

            # Calculating derivatives w.r.t Parameters
            D_m = (-2 / self.n) * sum(self.data * (self.label - y_pred))
            D_b = (-2 / self.n) * sum(self.label - y_pred)

            # Updating Parameters
            self.m = self.m - lr * D_m
            self.b = self.b - lr * D_b  # Fixed: changed from self.c to self.b

    def predict(self, inp):
        y_pred = self.m * inp + self.b
        return y_pred


# Loading the data
df = pd.read_csv('./data_LinearRegression.csv')

# Preparing the data
x = np.array(df.iloc[:, 0])
y = np.array(df.iloc[:, 1])

# Creating the class object
regressor = LinearRegression(x, y)

# Training the model with .fit method
regressor.fit(1000, 0.0001)  # epochs - 1000, learning_rate - 0.0001

# Predicting the values
y_pred = regressor.predict(x)

# Plotting the results
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='green', label='Data Points')
plt.plot(x, y_pred, color='k', lw=3, label='Regression Line')
plt.xlabel('x', size=20)
plt.ylabel('y', size=20)
plt.title('Linear Regression', size=24)
plt.legend()
plt.show()

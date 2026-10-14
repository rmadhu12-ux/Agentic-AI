from sklearn.linear_model import LinearRegression
import numpy as np

# Data: [Square Footage]
X = np.array([[600], [800], [1000], [1200], [1500]])
# Labels: [Price in thousands]
y = np.array([250, 310, 390, 450, 560])

# Initialize and train the model
model = LinearRegression()
model.fit(X, y)

# Predict the price for a 1100 sq ft house
prediction = model.predict([[1100]])
# print(f"Predicted Price: ${prediction[0]:.2f}k")
print (prediction)
from sklearn.cluster import KMeans
import numpy as np

# Data: [Spending Score (1-10), Visit Frequency (per month)]
X = np.array([
    [9, 8], [1, 2], [9, 9],  # Group 1: High spenders, frequent
    [2, 1], [8, 7], [2, 2],  # Group 2: Low spenders, infrequent
    [5, 5], [6, 4], [5, 6]   # Group 3: Average shoppers
])

# We tell the model to find 3 distinct groups
kmeans = KMeans(n_clusters=3, n_init=10)
kmeans.fit(X)

# See which group each data point was assigned to
print("Cluster Assignments:", kmeans.labels_)

# Predict the group for a new customer with score 8 and frequency 7
new_customer = kmeans.predict([[1, 1]])
print(f"New customer belongs to Cluster: {new_customer[0]}")
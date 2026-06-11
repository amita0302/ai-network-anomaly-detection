from sklearn.ensemble import IsolationForest
import numpy as np


# Training data (normal system behavior)
training_data = np.array([
    [30, 40],
    [35, 45],
    [40, 50],
    [45, 55],
    [50, 60]
])

# Create and train model
model = IsolationForest(contamination=0.1)

model.fit(training_data)

# Function to detect anomaly
def detect_anomaly(cpu, ram):

    test_data = np.array([[cpu, ram]])

    prediction = model.predict(test_data)

    if prediction[0] == -1:
        return "ANOMALY DETECTED"

    else:
        return "NORMAL"

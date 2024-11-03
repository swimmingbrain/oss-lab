import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier  # New classifier
from sklearn.model_selection import train_test_split
from matplotlib.lines import Line2D  # For custom legend
from sklearn.metrics import ConfusionMatrixDisplay

def load_wdbc_data(filename):
    data = []  # Shape: (569, 30)
    target = []  # Shape: (569, )
    target_names = ['malignant', 'benign']
    feature_names = [
        'mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness',
        'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry',
        'mean fractal dimension', 'radius error', 'texture error', 'perimeter error',
        'area error', 'smoothness error', 'compactness error', 'concavity error',
        'concave points error', 'symmetry error', 'fractal dimension error', 'worst radius',
        'worst texture', 'worst perimeter', 'worst area', 'worst smoothness',
        'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry',
        'worst fractal dimension'
    ]

    # Read data from file
    with open(filename) as f:
        for line in f.readlines():
            items = line.strip().split(',')
            # Convert labels: 'M' -> 0 (malignant), 'B' -> 1 (benign)
            target.append(0 if items[1] == 'M' else 1)
            # Convert features to floats
            data.append([float(x) for x in items[2:]])
    
    data = np.array(data)
    target = np.array(target)
    return data, target, target_names, feature_names

# Find file path
script_dir = os.path.dirname(__file__)
wdbc_path = os.path.join(script_dir, 'data', 'wdbc.data')

# Load the dataset
data, target, target_names, feature_names = load_wdbc_data(wdbc_path)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.3, random_state=42)

# Train a model using RandomForestClassifier
model = RandomForestClassifier(random_state=42)  # Chosen as the better classifier
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
accuracy = metrics.balanced_accuracy_score(y_test, y_pred)

# Visualize the confusion matrix
conf_matrix = metrics.confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=target_names)
disp.plot(cmap='viridis')
plt.title(f'Confusion Matrix (Accuracy: {accuracy:.3f})')
plt.show()

# Scatter plot to visualize classification results
cmap = np.array([(1, 0, 0), (0, 1, 0)])  # Red for malignant, green for benign
clabel = [Line2D([0], [0], marker='o', lw=0, label=target_names[i], color=cmap[i]) for i in range(len(cmap))]

# Visualize the first two features for simplicity
plt.figure()
plt.title(f'Classification Scatter Plot (Accuracy: {accuracy:.3f})')
plt.scatter(X_test[:, 0], X_test[:, 1], c=[cmap[label] for label in y_test], edgecolors=[cmap[pred] for pred in y_pred])
plt.xlabel(feature_names[0])  # mean radius
plt.ylabel(feature_names[1])  # mean texture
plt.legend(handles=clabel, framealpha=0.5)
plt.show()

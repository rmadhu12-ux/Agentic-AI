from sklearn.metrics import precision_score, recall_score, f1_score

# The real truth (what actually happened)
actual_labels = [1, 1, 1, 0, 0, 1, 0, 0, 0, 1]

# What our AI predicted
predicted_labels = [1, 1, 0, 0, 0, 1, 1, 0, 0, 1]

# Calculate metrics
precision = precision_score(actual_labels, predicted_labels)
recall = recall_score(actual_labels, predicted_labels)
f1 = f1_score(actual_labels, predicted_labels)

print(f"Precision: {precision:.2f}") # Accuracy of the "positive" guesses
print(f"Recall:    {recall:.2f}")    # Ability to find all "positive" cases
print(f"F1-Score:  {f1:.2f}")        # The balanced score
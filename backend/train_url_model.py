import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

from url_features import extract_features

#load data
df = pd.read_csv('backend/phishing_site_urls.csv')
print(f"Dataset size: {len(df)}")
print(df['Label'].value_counts())

##extract features
print("\nExtracting features (this may take a moment)...")
feature_list = []
for url in df['URL']:
    try:
        feature_list.append(extract_features(str(url)))
    except Exception:
        feature_list.append({})

X = pd.DataFrame(feature_list).fillna(0)
y = df['Label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Define models to compare which is best for our use case. We care most about precision (not flagging legit sites) and recall (catching phishing sites) 
# We will pick the best model based on a combination of these metrics
# Random Forest often performs well on data like this, but we will test several to be sure.
# Note: We use CalibratedClassifierCV for SVM so it can provide probabilities
models = {
    'Logistic Regression':    LogisticRegression(max_iter=1000),
    'Support Vector Machine': CalibratedClassifierCV(LinearSVC(max_iter=2000)),
    'Decision Tree':          DecisionTreeClassifier(),
    'Random Forest':          RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42),
    'Naive Bayes':            GaussianNB(),
    'K-Nearest Neighbor':     KNeighborsClassifier(),
}

#evaluate all models and store results in dictionaries for easy comparison later
accuracy, precision, recall, f1 = {}, {}, {}, {}

for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    accuracy[name]  = accuracy_score(y_test, preds)
    # 'bad' is the positive class (phishing)
    precision[name] = precision_score(y_test, preds, pos_label='bad')
    recall[name]    = recall_score(y_test, preds, pos_label='bad')
    f1[name]        = f1_score(y_test, preds, pos_label='bad')

    print(f"  [Result] F1-Score: {f1[name]:.3f} | Accuracy: {accuracy[name]:.3f}")

#results
df_results = pd.DataFrame({
    'F1-Score':  f1,
    'Accuracy':  accuracy,
    'Precision': precision,
    'Recall':    recall,
}).sort_values('F1-Score', ascending=False)

print("\nModel Performance Comparison:")
print(df_results)

#plot
ax = df_results.plot.barh(figsize=(10, 7))
ax.legend(ncol=2, bbox_to_anchor=(0, 1), loc='lower left')
plt.tight_layout()
plt.savefig('backend/model_comparison.png', dpi=150)
print("\nComparison plot saved to 'backend/model_comparison.png'")

# pick the best model based on F1-Score (balance of precision and recall) and show detailed evaluation
best_model_name = df_results.index[0]
best_model = models[best_model_name]

print(f"\n🏆 Best Model Selected: {best_model_name}")

# winner evaluation details
preds_best = best_model.predict(X_test)
TN, FP, FN, TP = confusion_matrix(y_test, preds_best, labels=['good', 'bad']).ravel()

print(f"\n--- Confusion Matrix for {best_model_name} ---")
print(f"  True Positives  (Caught Phishing): {TP}")
print(f"  False Positives (False Alarms):    {FP}")
print(f"  True Negatives  (Correctly Clean): {TN}")
print(f"  False Negatives (Missed Phishing): {FN}")
print("-" * 40)
print(classification_report(y_test, preds_best))

# save the best model and metadata for use in url_logic.py
print(f"\nSaving {best_model_name} as the production model...")

# create backend dir if it doesn't exist
os.makedirs('backend', exist_ok=True)

joblib.dump(best_model, 'backend/url_model.pkl')
joblib.dump(list(X.columns), 'backend/url_features_columns.pkl')
joblib.dump({'phishing_label': 'bad', 'legitimate_label': 'good'}, 'backend/url_label_map.pkl')

print(f"Successfully saved 'url_model.pkl' and metadata.")
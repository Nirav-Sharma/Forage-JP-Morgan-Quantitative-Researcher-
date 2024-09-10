import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc

df = pd.read_csv('Task 3 and 4_Loan_Data.csv')

df['payment_to_income'] = df['loan_amt_outstanding'] / df['income']
df['debt_to_income'] = df['total_debt_outstanding'] / df['income']

features = ['credit_lines_outstanding', 'debt_to_income', 'payment_to_income', 'years_employed', 'fico_score']
X = df[features]  # Predictor variables
y = df['default']  # Target variable (1 for default, 0 for no default)

log_reg = LogisticRegression(random_state=0, solver='liblinear', tol=1e-5, max_iter=10000)
log_reg.fit(X, y)

print("Model coefficients:", log_reg.coef_)
print("Model intercept:", log_reg.intercept_)

y_pred = log_reg.predict(X)

fpr, tpr, thresholds = roc_curve(y, y_pred)

error_rate = np.mean(np.abs(y - y_pred))
print("Error rate: {:.4f}".format(error_rate))

roc_auc = auc(fpr, tpr)
print("AUC score: {:.4f}".format(roc_auc))
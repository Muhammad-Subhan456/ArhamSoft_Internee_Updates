# Loan Default Prediction — Evaluation Report

## 1. Task

The objective was to build and evaluate a machine-learning pipeline
for predicting whether a loan applicant will default.

The dataset contains 1,200 synthetic loan applications with the
following predictors:

- Credit score
- Applicant income
- Loan amount
- Employment type

The target variable is `default`, where `1` represents a default and
`0` represents no default.

The data was split into training and test sets using an 80/20 stratified
split with `random_state=42`. Missing credit scores were handled using
the training-set median only.

The training-only credit-score imputation value was
**649.00**.

## 2. Baseline

A `DummyClassifier` using the `most_frequent` strategy was used as the
baseline.

The baseline achieved:

- Accuracy: **0.6000**
- Precision: **0.6000**
- Recall: **1.0000**
- F1: **0.7500**
- ROC-AUC: **0.5000**

The baseline predicts the majority class for every applicant. Its
ROC-AUC of **0.5000** shows that it provides
no meaningful ranking ability beyond chance.

Its recall of **1.0000** should therefore not
be interpreted as evidence of a strong model: the baseline achieves
this by predicting the majority class for everyone.

## 3. Model Comparison

The tuned models were evaluated on the same untouched held-out test set.


| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| baseline | 0.6000 | 0.6000 | 1.0000 | 0.7500 | 0.5000 |
| logistic_regression | 0.7458 | 0.7677 | 0.8264 | 0.7960 | 0.8454 |
| decision_tree | 0.7292 | 0.7651 | 0.7917 | 0.7782 | 0.8258 |
| random_forest | 0.7708 | 0.7834 | 0.8542 | 0.8173 | 0.8541 |


## 4. Final Model Selection

The selected final model is **random_forest**.

The Random Forest achieved:

- Accuracy: **0.7708**
- Precision: **0.7834**
- Recall: **0.8542**
- F1: **0.8173**
- ROC-AUC: **0.8541**

Compared with Logistic Regression, Random Forest achieved an accuracy
of **0.7708** versus
**0.7458**, and an F1 score of
**0.8173** versus
**0.7960**.

Random Forest also achieved higher ROC-AUC
(**0.8541**) than Logistic Regression
(**0.8454**).

Therefore, Random Forest was selected because it provided the strongest
overall held-out test performance among the trained machine-learning
models. The decision was not based on accuracy alone.

## 5. Error Analysis

The final Random Forest produced **34 false positives** and
**21 false negatives** on the held-out test set, resulting in
**55 total misclassified applicants**.

The average predicted default probability was
**0.659** for false positives and
**0.366** for false negatives.

The error analysis also examined credit score, applicant income,
loan amount, and employment type to identify potential patterns in the
misclassified cases.

The employment category with the highest observed overall test-set
error rate was **Self-Employed**, with an error rate of
**26.47%**.

This is an observation about the test sample rather than evidence that
employment type causes prediction errors.

## 6. Calibration

The Random Forest's predicted default probabilities were evaluated
using a calibration curve with 10 probability bins.

The mean absolute calibration gap was
**0.0517**, while the maximum observed
calibration gap was **0.1705**.

Calibration is different from ROC-AUC. ROC-AUC evaluates how well the
model separates and ranks defaults versus non-defaults, while
calibration evaluates whether predicted probabilities correspond to
observed default frequencies.

Because the model is being evaluated on synthetic data and a single
held-out test set, its probabilities should not automatically be
treated as reliable real-world risk probabilities.

## 7. Honest Limitation

A major limitation is that the dataset does not contain important
real-world lending information such as an applicant's existing debt
obligations or debt-to-income ratio.

Without this information, the model has an incomplete view of an
applicant's ability to repay a loan. In addition, the dataset is
synthetic, so strong test-set performance does not establish that the
model would perform similarly on real lending data.

The model should therefore be treated as an assessment pipeline rather
than a production-ready lending decision system.

## 8. Conclusion

The final pipeline used train-only preprocessing, a stratified
train/test split, a dummy baseline, tuned Logistic Regression,
Decision Tree, and Random Forest models, held-out test evaluation,
error analysis, and calibration analysis.

Random Forest was selected as the final model because it produced the
strongest overall test-set performance among the trained models,
achieving an F1 score of **0.8173** and
ROC-AUC of **0.8541**.

The evaluation also demonstrates that strong classification metrics do
not by themselves establish that predicted probabilities are suitable
for real-world financial decisions.
